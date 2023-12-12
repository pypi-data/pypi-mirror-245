# -*- coding: UTF-8 -*-

# 执行成功
errno_success = 0
# qmt错误码基数
qmt_errno_base = 1000
# miniQMT 没有找到
errno_miniqmt_not_found = qmt_errno_base + 1
# quant1x.yaml配置文件没找到
errno_config_not_exist = qmt_errno_base + 2
# 连接miniQMT失败
errno_miniqmt_connect_failed = qmt_errno_base + 3
# 非交易日
errno_not_trade_day = qmt_errno_base + 4
# 缺少账户id
errno_not_found_account_id = qmt_errno_base + 5
# 缺少订单路径
errno_not_found_order_path = qmt_errno_base + 6

kFormatFileDate = '%Y%m%d'
kFormatOnlyDate = '%Y-%m-%d'
kFormatTimestamp = '%Y-%m-%d %H:%M:%S'
kTimestamp = '%H:%M:%S'
errBadSymbol = RuntimeError("无法识别的证券代码")
