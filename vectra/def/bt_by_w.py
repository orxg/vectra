# -*- coding: utf-8 -*-
"""
Created on Thu Mar 08 11:12:04 2018

@author: ldh
"""

from vectra.api import order_pct_to

def initilize(context):
    print context.weight_map
    pass

def before_trading(context):
    pass

def handle_bar(context,bar_map):
    current_date = context.current_date.strftime('%Y%m%d')    
    try:
        target_weight = context.weight_map.loc[current_date]
    except:
        return
    
    current_weight = context.account.get_weight()
    weight_change = target_weight - current_weight
    sell_sec_ser = weight_change.loc[weight_change < 0.0]
    buy_sec_ser = weight_change.loc[weight_change > 0.0]

    for sec in sell_sec_ser.index.tolist():
        order_pct_to(sec,target_weight[sec])
    for sec in buy_sec_ser.index.tolist():
        order_pct_to(sec,target_weight[sec])

def after_trading(context):
    pass

