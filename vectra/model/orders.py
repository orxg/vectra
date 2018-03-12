# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:16:27 2017

@author: LDH
"""

# orders.py

from ..utils import id_gen
from ..constants import ORDER_STATUS

class Order():
    order_id_gen = id_gen()
    
    def __init__(self):
        '''
        Attributes
        ----------
        order_id
            订单唯一id
        calendar_dt
            datetime 交易日日期
        trading_dt
            datetime 交易日时间
        ticker
            代码
        amount
            数量
        direction
            方向
        order_price
            出价
        order_state
            系统常量,订单状态
        fill_dt
            datetime 成交时间
        tax
            税费
        commission_fee
            交易佣金费用
        transfer_fee
            过户费
        transaction_fee
            交易费用
        match_price
            成交价
        match_amount
            成交数量
        '''
        self.order_id = None
        
        self.calendar_dt = None
        self.trading_dt = None
        self.ticker = None
        self.amount = None
        self.direction = None
        self.order_price = None
        
        self.order_state = None
        self.fill_dt = None
        self.tax = None
        self.commission_fee = None
        self.transfer_fee = None
        self.transaction_fee = None
        self.match_price = None  
        self.match_amount = None         
        
    def get_state(self):
        return {'order_id':self.order_id,
                'calendar_dt':self.calendar_dt,
                'trading_dt':self.trading_dt,
                'ticker':self.ticker,
                'amount':self.amount,
                'direction':self.direction,
                'order_price':self.order_price,
                
                'order_state':self.order_state,
                'fill_dt':self.fill_dt,
                'tax':self.tax,
                'commission_fee':self.commission_fee,
                'transfer_fee':self.transfer_fee,
                'transaction_fee':self.transaction_fee,
                'match_price':self.match_price,
                'match_amount':self.match_amount}
        
    def set_state(self,state):
        self.order_id = state['order_id']
        self.calendar_dt = state['calendar_dt']
        self.trading_dt = state['trading_dt']
        self.ticker = state['ticker']
        self.amount = state['amount']
        self.direction = state['direction']
        self.order_price = state['order_price']
        
        self.order_state = state['order_state']
        self.fill_dt = state['fill_dt']
        self.tax = state['tax']
        self.commission_fee = state['commission_fee']
        self.transfer_fee = state['transfer_fee']
        self.transaction_fee = state['transaction_fee']
        self.match_price = state['match_price']
        self.match_amount = state['match_amount']
        
    @classmethod 
    def __create_order__(cls,calendar_dt,trading_dt,ticker,
                 amount,direction,order_price,order_state = None,
                 fill_dt = None,tax = None,commission_fee = None,
                 transfer_fee = None,transaction_fee = None,
                 match_price = None,match_amount = None):
        order = cls()
        
        order.order_id = next(order.order_id_gen)
        
        order.calendar_dt = calendar_dt
        order.trading_dt = trading_dt
        order.ticker = ticker
        order.amount = amount
        order.direction = direction
        order.order_price = order_price
        
        order.order_state = ORDER_STATUS.PENDING_NEW
        
        order.fill_dt = fill_dt
        order.tax = tax
        order.commission_fee = commission_fee
        order.transfer_fee = transfer_fee
        order.transaction_fee = transaction_fee
        order.match_price = match_price   
        order.match_amount = match_amount
        return order