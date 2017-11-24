# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 13:23:37 2017

@author: FSB
"""

# simulation_broker.py

from vectra.constants import DIRECTION_LONG,DIRECTION_SHORT
from vectra.events import EVENT,Event
from vectra.model.orders import FillOrder

class SimulationBroker():
    def __init__(self,env):
        self.env = env
        self.blotter = []
        
        event_bus = env.event_bus
        event_bus.add_listener(EVENT.PENDING_NEW_ORDER,self._collect_order)
        event_bus.add_listener(EVENT.BAR,self._match_on_bar)
        event_bus.add_listener(EVENT.KILL_ORDER,self._handle_kill_order)
        
    #%% 监听函数
    def _collect_order(self,event):
        order = event.order
        # 检查可交易性
        if self._tradable_check(order):
            self.blotter.append(order)
            self.env.event_bus.publish_event(Event(EVENT.PENDING_NEW_ORDER_PASS,
                                             order = order))
        else:
            self.env.event_bus.publish_event(Event(EVENT.REJECT_ORDER,
                                             order = order,reason = 'Can not trade'))            
    def _match_on_bar(self,event):
        self._match()
             
    def _handle_kill_order(self,event):
        '''
        需要实现订单id属性,此处暂不实现。
        '''
        pass
    
    #%% 订单检查
    def _tradable_check(self,order):
        '''
        检查标的是否当天可交易。
        '''
        ticker = order.ticker
        date = order.calendar_dt
        return self.env.data_proxy.if_tradable(ticker,date)
    
    #%% 订单撮合
    def _match(self):
        '''
        按照blotter中的顺序逐一检查订单是否合法,
        若合法,则生成TRADE事件并广播。
        若不合法,则生成REJECT_ORDER并广播。
        '''
        
        while self.blotter: 
            order = self.blotter.pop(0)
            calendar_dt = order.calendar_dt
            trading_dt = order.trading_dt
            ticker = order.ticker
            amount = order.amount
            direction = order.direction
            order_price = order.order_price
            
            # 账户检验
            if direction == DIRECTION_LONG:
                tax = 0
                transfer_fee = int(amount/1000 - 0.001) + 1
                commission_fee = max(amount * order_price * 0.003,5)
                transaction_fee = tax + transfer_fee + commission_fee                
                cash = self.env.account.cash
                
                if cash < amount * order_price + transaction_fee:
                    reject_event = Event(EVENT.REJECT_ORDER,
                     reason = 'Not enough cash',
                     order = order)
                    self.env.event_bus.publish_event(reject_event)
                    return
                    
                
            elif direction == DIRECTION_SHORT:
                tax = amount * order_price * 0.001
                transfer_fee = int(amount/1000 - 0.001) + 1
                commission_fee = max(amount * order_price * 0.003,5)
                transaction_fee = tax + transfer_fee + commission_fee
                
                position = self.env.account.get_position(ticker)
                
                if amount > position:
                    reject_event = Event(EVENT.REJECT_ORDER,
                     reason = 'Not enough stocks to sell',
                     order = order)
                    self.env.event_bus.publish_event(reject_event)
                    return                    
            
            # 市场检验
            high_price = self.env.bar_map.get_stock_latest_bar_value(ticker,'high_price')
            low_price = self.env.bar_map.get_stock_latest_bar_value(ticker,'low_price')
            total_amount = self.env.bar_map.get_stock_latest_bar_value(ticker,'amount')
            
            if order_price >= high_price:
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order price is too high',
                 order = order)
                self.env.event_bus.publish_event(reject_event)  
                return
            if order_price <= low_price:
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order price is too low',
                 order = order)
                self.env.event_bus.publish_event(reject_event)
                return
            if amount >= total_amount:
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order amount is too much',
                 order = order)
                self.env.event_bus.publish_event(reject_event) 
                return
                
            # 生成交易订单
            fill_order_obj = FillOrder(calendar_dt,trading_dt,
                                       ticker,amount,
                                       direction,tax,
                                       commission_fee,transfer_fee,
                                       transaction_fee,
                                       order_price)
            trade_event = Event(EVENT.TRADE,calendar_dt = calendar_dt,
                               trading_dt = trading_dt,order = fill_order_obj)
            
            self.env.event_bus.publish_event(trade_event)                      
          
       
        
        
    