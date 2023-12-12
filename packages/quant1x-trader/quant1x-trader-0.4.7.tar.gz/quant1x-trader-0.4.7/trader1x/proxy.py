# -*- coding: UTF-8 -*-
import base1x
from base1x import market

module = 'trader1x'

base1x.redirect(module, __file__)

import sys

import uvicorn
from fastapi import FastAPI, Form
from path import Path
from xtquant import xtconstant

from trader1x import thinktrader, config, utils, context
from base1x.logger import logger
from pathlib import Path

__application_proxy = 'quant1x-proxy'

order_status = {
    xtconstant.ORDER_UNREPORTED: '未报',
    xtconstant.ORDER_WAIT_REPORTING: '待报',
    xtconstant.ORDER_REPORTED: '已报',
    xtconstant.ORDER_REPORTED_CANCEL: '已报待撤',
    xtconstant.ORDER_PARTSUCC_CANCEL: '部成待撤',
    xtconstant.ORDER_PART_CANCEL: '部撤',
    xtconstant.ORDER_CANCELED: '已撤',
    xtconstant.ORDER_PART_SUCC: '部成',
    xtconstant.ORDER_SUCCEEDED: '已成',
    xtconstant.ORDER_JUNK: '废单',
    xtconstant.ORDER_UNKNOWN: '未知'
}

# 操作 - 状态码 - 成功
OPERATION_STATUS_SUCCESS = 0
# 操作 - 信息 - 成功
OPERATION_MESSAGE_SUCCESS = 'success'
# 操作 - 状态码 - 未知
OPERATION_STATUS_UNKNOWN = 999
# 操作 - 信息 - 未知
OPERATION_MESSAGE_UNKNOWN = 'unknown'

__uri_prefix = '/qmt'
app = FastAPI(root_path=__uri_prefix)


@app.on_event('startup')
async def proxy_init():
    """
    代理初始化
    :return:
    """
    # global __config
    global __context, __trader
    logger.info('{} start...', __application_proxy)
    # 1. 获取配置信息
    __config = config.load()
    __trader = thinktrader.ThinkTrader(__config)
    # 2. 连接miniQMT
    connect_result = __trader.set_trader()
    if connect_result == 0:
        logger.info('connect miniQmt: success')
    else:
        logger.error('connect miniQmt: failed')
        return utils.errno_miniqmt_connect_failed
    logger.info('{} start...OK', __application_proxy)
    # 3. 设置账号
    __context = context.QmtContext(__config)
    __trader.set_account(__context.account_id)
    single_funds_available = __trader.single_available(__config.max_stock_quantity_for_strategy)
    logger.warning('今天, 单一策略最大可买{}个标的, 每标的可用金额{}', __config.max_stock_quantity_for_strategy,
                   single_funds_available)


@app.on_event('shutdown')
async def proxy_shutdown():
    """
    代理关闭
    :return:
    """
    logger.info('{} shutdown...', __application_proxy)
    __trader.stop()
    logger.info('{} shutdown...OK', __application_proxy)


@app.api_route(__uri_prefix + '/health')
async def hello(name: str = 'anonymous'):
    """
    探测服务接口(√)
    :param name:
    :return:
    """
    return {rf'hello, {name}'}


@app.api_route(__uri_prefix + '/query/asset', methods=['GET', 'POST'])
async def query_assets():
    """
    查询总资产(√)
    """
    asset = __trader.query_asset()
    return {"total_asset": asset.total_asset,
            "cash": asset.cash,
            "market_value": asset.market_value,
            "frozen_cash": asset.frozen_cash
            }


@app.api_route(__uri_prefix + '/query/holding', methods=['GET', 'POST'])
async def query_holding():
    """
    查询当前持仓(√)
    """
    holding = []
    for p in __trader.query_positions():
        holding.append(
            {'account_type': p.account_type,
             'account_id': p.account_id,
             'stock_code': p.stock_code,
             'volume': p.volume,
             'can_use_volume': p.can_use_volume,
             'open_price': base1x.fix_float(p.open_price),
             'market_value': base1x.fix_float(p.market_value),
             'frozen_volume': p.frozen_volume,
             'on_road_volume': p.on_road_volume,
             'yesterday_volume': p.yesterday_volume,
             'avg_price': p.avg_price,
             }
        )
    return holding


@app.api_route(__uri_prefix + '/query/trade', methods=['GET', 'POST'])
async def query_trade():
    """
    查询当日成交(√)
    """
    trades = __trader.query_trades()
    result = []
    for trade in trades:
        result.append(
            {'stock_code': trade.stock_code,
             'order_type': trade.order_type,
             'traded_volume': trade.traded_volume,
             'traded_price': trade.traded_price,
             'traded_amount': trade.traded_amount,
             'traded_time': base1x.seconds_to_timestamp(trade.traded_time),
             "traded_id": trade.traded_id, "order_sysid": trade.order_sysid})
    return result


@app.api_route(__uri_prefix + '/query/order', methods=['GET', 'POST'])
async def query_order(order_id: str = ''):
    """
    查询当日委托(√)
    """
    order_id = order_id.strip()
    if order_id == '' or order_id == '0':
        orders = __trader.query_orders()
    else:
        order = __trader.query_order(int(order_id))
        # 订单不存在，下单失败
        if order is None:
            return []
        orders = [order]
    result = []
    for order in orders:
        result.append(
            {'account_type': order.account_type,
             'account_id': order.account_id,
             'order_time': base1x.seconds_to_timestamp(order.order_time),
             'stock_code': order.stock_code,
             'order_type': order.order_type,
             'price': order.price,
             'price_type': order.price_type,
             'order_volume': order.order_volume,
             'order_id': order.order_id,
             "order_sysid": order.order_sysid,
             'traded_price': order.traded_price,
             'traded_volume': order.traded_volume,
             'order_status': order.order_status,
             'status_msg': order.status_msg,
             'strategy_name': order.strategy_name,
             'order_remark': order.order_remark,
             }
        )
    return result


def throw_error(status: int, message: str) -> dict:
    """
    抛出错误
    :param status: 状态码, 0-成功, 非0-失败
    :param message: 错误信息
    :return:
    """
    return {'status': status, 'message': message}


@app.api_route(__uri_prefix + '/trade/order', methods=['POST'])
async def trade_place_order(direction: str = Form(),
                            code: str = Form(),
                            price: str = Form(),
                            volume: str = Form(),
                            strategy: str = Form(),
                            remark: str = Form()
                            ):
    """
    下单(√), 参数有:
    direction: 交易方向, buy, sell
    code: 证券代码, 格式:{code}.{marker_id}
    price: 价格, 单位是元
    volume: 数量, 单位是股
    strategy: 策略名称
    remark: 订单备注
    """
    order_errno = 10000
    status = OPERATION_STATUS_SUCCESS
    message = OPERATION_MESSAGE_SUCCESS
    # 1. 交易方向
    direction = direction.strip()
    if direction == 'buy':
        # 1.1 买入
        trade_direction = xtconstant.STOCK_BUY
    elif direction == 'sell':
        # 1.2 卖出
        trade_direction = xtconstant.STOCK_SELL
    else:
        # 1.3 方向错误
        return throw_error(order_errno + 10, '交易方向错误')
    # 2. 证券代码
    code = code.strip()
    if code == '':
        return throw_error(order_errno + 20, '证券代码不能为空')
    elif len(code) != 9:
        return throw_error(order_errno + 21, '非A股证券代码长度')
    elif not code.endswith(market.tup_market):
        return throw_error(order_errno + 22, '交易所简写错误')
    stock_code = code
    # 3. 数量
    volume = volume.strip()
    if volume == '':
        return throw_error(order_errno + 30, '交易数量不能为空')
    stock_volume = int(volume)
    if stock_volume % 100 != 0:
        return throw_error(order_errno + 31, '交易数量非100股的整数倍')
    # 4. 价格
    price = price.strip()
    if price == '':
        return throw_error(order_errno + 40, '委托价格不能为空')
    stock_price = float(price)
    if stock_price <= 1.000:
        return throw_error(order_errno + 41, '委托价格不能出现小于等于1.000元')
    # 5. 策略名称
    strategy = strategy.strip()
    if strategy == '':
        return throw_error(order_errno + 50, '策略名称不能为空')
    strategy_name = strategy
    # 6. 订单备注
    remark = remark.strip()
    if remark == '':
        return throw_error(order_errno + 60, '订单备注不能为空')
    if len(remark.encode('utf-8')) > 24:
        return throw_error(order_errno + 61, '订单备注不能超过24个字节')
    order_remark = remark
    # 7. 执行同步委托下单
    order_id = __trader.order(stock_code, trade_direction, stock_volume, xtconstant.FIX_PRICE, stock_price,
                              strategy_name, order_remark)
    logger.warning('order[{}]: code={}, direction={}, price={}, volume={}, strategy_name={}, order_remark={}', order_id,
                   stock_code, direction, stock_price, stock_volume, strategy_name, order_remark)
    return {'status': status, 'message': message, 'order_id': order_id}


@app.api_route(__uri_prefix + '/trade/cancel', methods=['POST'])
async def trade_cancel_order(order_id: str = Form()):
    """
    撤单(√)
    """
    cancel_errno = 20000
    order_id = order_id.strip()
    if order_id == '':
        return throw_error(cancel_errno + 1, 'order_id不能为空')
    elif not order_id.isdigit():
        return throw_error(cancel_errno + 2, 'order_id必须是整型')
    cancel_order_id = int(order_id)
    if cancel_order_id <= 0:
        return throw_error(cancel_errno + 3, 'order_id必须大于0')
    result = __trader.cancel(cancel_order_id)
    logger.warning(f'order_id={order_id}, errno={result}')
    # 返回撤单成功或者失败, 0: 成功, -1: 委托已完成, -2: 未找到对应委托编号, -3: 账号未登陆
    if result == 0:
        return throw_error(OPERATION_STATUS_SUCCESS, OPERATION_MESSAGE_SUCCESS)
    elif result == -1:
        return throw_error(cancel_errno + 4, '委托已完成')
    elif result == -2:
        return throw_error(cancel_errno + 5, '未找到对应委托编号')
    elif result == -3:
        return throw_error(cancel_errno + 6, '账号未登陆')
    else:
        logger.warning(f'cancel: order_id={order_id}, 未知错误, errno={result}')
    return throw_error(cancel_errno + OPERATION_STATUS_UNKNOWN, OPERATION_MESSAGE_UNKNOWN)


def sign(enable: bool = True):
    """
    验签 - 函数装饰器(aspect)
    TODO: 具体验签方式未完成
    :param enable: 是否启用验签, 默认启用验签
    :return:
    """

    def count_time(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return count_time


def proxy() -> int:
    # 1. 加载配置文件
    logger.info('加载配置...')
    __config = config.load()
    logger.info('配置信息: {}', __config)
    logger.info('加载配置...OK')
    # 2. 配置路由
    # app.include_router(prefix=__uri_prefix)
    # 3. 启动服务
    logger.warning('{} start http server[{}:{}]...', __application_proxy, __config.proxy_address, __config.proxy_port)
    uvicorn.run(app=f'{module}.{Path(__file__).stem}:app', host=__config.proxy_address, port=__config.proxy_port,
                workers=__config.proxy_workers,
                reload=True, debug=True)
    return 0


# class ProxyService(SMWinservice):
#     _svc_name_ = 'quant1x-qmt-proxy'
#     _svc_display_name_ = 'Quang1X-miniQMT-Proxy'
#     _svc_description_ = 'Quant1X miniQMT 代理服务'
#
#     def __init__(self, args):
#         super().__init__(args)
#         self.isrunning = None
#
#     def start(self):
#         self.isrunning = True
#
#     def stop(self):
#         self.isrunning = False
#
#     def main(self):
#         proxy()
#
#
# if __name__ == '__main__':
#     ProxyService.parse_command_line()

if __name__ == '__main__':
    sys.exit(proxy())
