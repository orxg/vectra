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

#%% 订单状态
class ORDER_STATUS(CustomEnum):
    PENDING_NEW = "PENDING_NEW"
    ACTIVE = "ACTIVE"
    FILLED = "FILLED"
    PARTIAL_FILLED = 'PARTIAL_FILLED'
    REJECTED = "REJECTED"
    PENDING_CANCEL = "PENDING_CANCEL"
    CANCELLED = "CANCELLED"