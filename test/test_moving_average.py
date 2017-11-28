# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 08:59:24 2017

@author: ldh
"""

# test_moving_average.py

from vectra.api import order_pct_to

import talib

def initilize(context):
    context.long_period = 30
    context.short_period = 5

def handle_bar(context,bar_map):
    universe = context.universe
    # 得到universe中股票的过去n个交易日收盘价数据
    his = bar_map.get_history('close_price',context.long_period)
    account = context.account
    buy_list = []
    sell_list = []
    
    try:
        for ticker in universe:
            ma_5 = talib.MA(his[ticker].values,context.short_period)[-1]
            ma_30 = talib.MA(his[ticker].values,context.long_period)[-1]
            
            if ma_5 is None or ma_30 is None:
                return
            
            if ma_5 >= ma_30 and account.get_position(ticker) == 0:
                buy_list.append(ticker)
                print ticker,context.current_date,ma_5,ma_30
                    
            if ma_5 < ma_30 and account.get_position(ticker) > 0:
                sell_list.append(ticker)
                print ticker,context.current_date,ma_5,ma_30
    except:
        return
            
    for ticker in sell_list:
        order_pct_to(ticker,0)
    
    for ticker in buy_list:
        order_pct_to(ticker,0.3)
        
        
    
