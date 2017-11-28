# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 08:30:40 2017

@author: ldh
"""

# test_buy_and_hold.py
from vectra.api import order_pct_to

def initilize(context):
    print 'IT IS INITILIZING!!!'
    context.fired = False
    context.flag = 0
    
def before_trading(context):
    context.signal_post_before_trading = 'This is a test'
    
def handle_bar(context,bar_map):
    hist = bar_map.get_history('close_price',5)
    print hist
#==============================================================================
#     print context.current_date
#     context.flag += 1
#     if not context.fired:
#         for ticker in context.universe:
#             order_pct_to(ticker,0.3)
#         context.fired = True
#==============================================================================
    
def after_trading(context):
    context.signal_post_after_trading = 'We have bought the stock'



