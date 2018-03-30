# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 09:02:46 2017

@author: ldh
"""

# constants.py

from enum import Enum

class CustomEnum(Enum):
    def __repr__(self):
        return '%s'%(self._name_)
    
#%% 回测模式
EASY_MODE = 'EASY_MODE'# 前复权回测
HARD_MODE = 'HARD_MODE'# 不复权回测

#%% 运行类型
BACKTEST = 'BACKTEST'
PAPER_TRADING = 'PAPER_TRADING'

#%% 交易方向
DIRECTION_LONG = 'DIRECTION_LONG'
DIRECTION_SHORT = 'DIRECTION_SHORT'

#%% 数据源
DATA_SOURCE_EXCEL = 'excel'
DATA_SOURCE_SQL = 'sql'
DATA_SOURCE_BCOLZ = 'bcolz'
#%% 订单状态
class ORDER_STATUS(CustomEnum):
    PENDING_NEW = "PENDING_NEW"
    ACTIVE = "ACTIVE"
    FILLED = "FILLED"
    PARTIAL_FILLED = 'PARTIAL_FILLED'
    REJECTED = "REJECTED"
    PENDING_CANCEL = "PENDING_CANCEL"
    CANCELLED = "CANCELLED"

#%% 交易费用
TRANSACTION_FEE_ITEMS = ['transfer_fee_on_long','transfer_fee_on_short',
                         'tax_rate_long','tax_rate_short',
                         'commission_fee_rate_long','commission_fee_rate_short',
                         'min_amount_long','min_amount_short']
TRANSACTION_FEE_DEFAULTS = [1,1,0,0.001,0.003,0.003,100,1]
