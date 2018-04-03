# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 13:14:33 2017

@author: ldh
"""

# api.py

__all__ = [
       'order',
       'order_to',
       'order_pct_to'
       ]

from ..constants import DIRECTION_LONG,DIRECTION_SHORT
from ..events import EVENT,Event
from ..environment import Environment
from ..model.orders import Order

def order(ticker,amount,order_price = None):
    '''
    下单函数。在handle_bar中调用。
    
    Parameters
    -----------
    ticker
        标的代码
    amount
        下单数量(股数),正负号代表方向
    order_price
        下单价格,默认为None,采取开盘价
    '''
    env = Environment.get_instance()
    
    amount = int(amount / 100) * 100 # 100的整数倍调整
    
    if amount < 0:
        direction = DIRECTION_SHORT
    elif amount > 0:
        direction = DIRECTION_LONG
    elif amount == 0:
        return 
    
    if order_price is None:       
        open_price =  env.bar_map.get_stock_latest_bar_value(ticker,'open_price')
        order_price = open_price
        
    order_obj = Order.__create_order__(env.calendar_dt,env.trading_dt,
                      ticker,abs(amount),
                      direction,order_price)
    order_event = Event(EVENT.PENDING_NEW_ORDER,
                        order = order_obj)
    
    env.event_bus.publish_event(order_event)
    return order_obj
    
def order_to(ticker,amount,order_price = None):
    '''
    下单函数。下单到指定数量。在handle_bar中调用。
    
    Parameters
    -----------
    ticker
        标的代码
    amount
        下单达到的数量(股数),正负号代表方向
    order_price
        下单价格,默认为None,采取开盘价
    '''
    env = Environment.get_instance()
    current_amount = env.account.get_position(ticker)
    delta_amount = amount - current_amount
    order(ticker,delta_amount,order_price)

def order_pct_to(ticker,pct,order_price = None):
    '''
    下单函数。下单到指定比例。在handle_bar中调用。
    
    Parameters
    -----------
    ticker
        标的代码
    pct
        下单达到的比例(相对于账户总价值)
    order_price
        下单价格,默认为None,采取开盘价
    
    Notes
    -------
    由于交易费用的存在,当pct为1的时候可能无法成交,
    所以需要在原比例上进行一定的调低以满足手续费要求。
    '''
    env = Environment.get_instance()
    account_value = env.account.total_account_value
    target_value = account_value * pct 

    if order_price is None:       
        open_price =  env.bar_map.get_stock_latest_bar_value(ticker,'open_price')
        order_price = open_price   
    if order_price == 0:
        print 'No data available for the trade for %s'%ticker
        return
    target_amount = int(target_value / order_price)
    
    order_to(ticker,target_amount,order_price)
    
    