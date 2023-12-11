# -*- coding: utf-8 -*-
__version__ = "2023.0.0.0"
__author__ = "Yitong Gong"

__doc__ = """
ZYYA-Codes - 一个中邮永安人写的python库
"""
from ZYYA_Codes.Net_Value.api import (
    net_value_fetch,
    RiskIndex
)

from ZYYA_Codes.market_data_api import (
    tushare_pro_api,
    tushare_set_token
)

from ZYYA_Codes.product_profit_decomposition import (
    read_GZB,
)

from ZYYA_Codes.utils import (
    set_configs,
    get_configs,
)


__all__ = [
    "net_value_fetch",
    "RiskIndex",
    "tushare_pro_api",
    "tushare_set_token",
    "read_GZB",
    "set_configs",
    "get_configs"
]

