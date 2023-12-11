# -*- coding: UTF-8 -*-
import os
import sys
import warnings
from dataclasses import dataclass

import base1x
import yaml
from base1x import TradingSession
from base1x.logger import logger

from trader1x import env, utils

warnings.filterwarnings('ignore')


@dataclass
class TraderConfig:
    """
    配置信息
    """
    # 账号ID
    account_id: str = ''
    # 运行路径
    order_path: str = ''
    # 时间范围 - 早盘策略
    head_time: TradingSession = TradingSession("09:27:00~14:57:00")
    # 时间范围 - 尾盘策略
    tail_time: TradingSession = TradingSession("14:45:00~14:59:50")
    # 时间范围 - 盘中订单
    tick_time: TradingSession = TradingSession("09:39:00-14:57:00")
    # 时间范围 - 持仓卖出
    ask_time: TradingSession = TradingSession("09:50:00~14:59:30")
    # 时间范围 - 撤销订单
    cancel_time: TradingSession = TradingSession("09:15:00~09:19:59, 09:30:00~14:56:59")
    # 时间范围 - 盘后复盘
    review_time: TradingSession = TradingSession("00:00:00~08:30:00, 15:01:00~23:59:59")
    # 买入持仓率, 资金控制阀值
    position_ratio: float = 0.5000
    # TODO: 废弃, 买入交易费率
    buy_trade_rate: float = 0.0250
    # TODO: 废弃, 相对开盘价溢价多少买入
    buy_premium_rate: float = 0.0200
    # 印花税 - 买入, 按照成交金额, 买入0.0%
    stamp_duty_rate_for_buy: float = 0.0000
    # 印花税 - 卖出, 按照成交金额, 卖出0.1%
    stamp_duty_rate_for_sell: float = 0.0010
    # 过户费 - 双向, 按照数量收取, 默认万分之六, 0.06%
    transfer_rate: float = 0.0006
    # 券商佣金 - 双向, 按成交金额计算, 默认万分之二点五, 0.025%
    commission_rate: float = 0.00025
    # 券商佣金最低, 默认5.00
    commission_min: float = 5.00
    # 保留现金
    keep_cash: float = 10000.00
    # tick订单最大金额, 默认20000.00
    tick_order_max_amount: float = 20000.00
    # tick订单最小金额, 默认10000.00
    tick_order_min_amount: float = 10000.00
    # 买入最大金额
    buy_amount_max: float = 250000.00
    # 买入最小金额
    buy_amount_min: float = 1000.00
    # 每策略最多可买股票数量, 这里默认3
    max_stock_quantity_for_strategy: int = 3
    # 自动卖出, 默认为True
    sell_order_auto: bool = True
    # 自动交易head订单, 默认为True
    head_order_auto: bool = True
    # 自动交易tick订单, 默认为True
    tick_order_auto: bool = True
    # 自动交易tail订单, 默认为True
    tail_order_auto: bool = True

    # 启动了mimiQMT机器的代理服务的监听地址, 默认为回环地址127.0.0.1, 强烈不推荐使用0.0.0.0
    proxy_address: str = base1x.lan_address()
    # 代理服务的监听端口, 默认18168
    proxy_port: int = 18168
    # 代理服务默认工作线程数, 默认为cpu核数的二分之一
    proxy_workers: int = base1x.max_procs()
    proxy_url: str = ""

    def __fix_instance(self):
        """
        加载后修复
        :return:
        """
        if isinstance(self.ask_time, str):
            ts = TradingSession(self.ask_time)
            if ts.is_valid():
                self.ask_time = ts
        if isinstance(self.cancel_time, str):
            ts = TradingSession(self.cancel_time)
            if ts.is_valid():
                self.cancel_time = ts
        if isinstance(self.tick_time, str):
            ts = TradingSession(self.tick_time)
            if ts.is_valid():
                self.tick_time = ts

    def __post_init__(self):
        """
        __init__()后调用, 调整类型
        :return:
        """
        self.__fix_instance()


# 全局变量 - 配置
__global_config = TraderConfig()


def load() -> TraderConfig:
    """
    加载配置文件
    :return:
    """
    global __global_config
    config = TraderConfig()
    config_filename = env.get_quant1x_config_filename()
    logger.info(config_filename)
    if not os.path.isfile(config_filename):
        logger.error('QMT config {}: 不存在', config_filename)
        sys.exit(utils.errno_config_not_exist)
    try:
        with open(config_filename, 'r', encoding='utf-8') as f:
            result = yaml.load(f, Loader=yaml.FullLoader)
            key_trader = "trader"
            if isinstance(result, dict) and key_trader in result:
                config = TraderConfig(**result[key_trader])
            config.account_id = str(result['order']['account_id'])
            config.order_path = str(result['order']['order_path'])
            config.max_stock_quantity_for_strategy = result['order']['top_n']
    except Exception as e:
        logger.error(f"发生了一个错误：{config_filename}\n错误信息：{e}")
        logger.warning('系统将使用默认配置')
        config = TraderConfig()
    # finally:
    #     logger.warning('系统将使用默认配置')
    # 检查重点配置
    if config.account_id == '':
        logger.error('配置缺少账户id')
        sys.exit(utils.errno_not_found_account_id)
    if config.order_path == '':
        logger.error('配置缺少订单路径')
        sys.exit(utils.errno_not_found_order_path)
    __global_config = config
    return config


def get() -> TraderConfig:
    global __global_config
    return __global_config


if __name__ == '__main__':
    config = load()
    print(config)
