# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 13:23:37 2017

@author: FSB
"""

# simulation_broker.py
import logging

from vectra.constants import DIRECTION_LONG,DIRECTION_SHORT,ORDER_STATUS
from vectra.events import EVENT,Event

class SimulationBroker():
    def __init__(self,env):
        self.env = env
        self.fee_table = env.fee_table
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
            order.order_state = ORDER_STATUS.ACTIVE
            self.blotter.append(order)
            self.env.event_bus.publish_event(Event(EVENT.PENDING_NEW_ORDER_PASS,
                                             order = order))
        else:
            order.order_state = ORDER_STATUS.REJECTED
            self.env.event_bus.publish_event(Event(EVENT.REJECT_ORDER,
                                             order = order,reason = 'Can not trade'))            
    def _match_on_bar(self,event):
        logging.info('MATCH ON BAR WHEN %s'%(self.env.calendar_dt))
        self._match()
        if len(self.blotter) != 0:
            logging.info('WARNING: THE BLOTTER IS NOT CLEAR ON %s'%(self.env.calendar_dt))
             
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
                cash = self.env.account.cash
                
                tax = abs(amount) * order_price * \
                    self.fee_table.loc[ticker,'tax_rate_long']
                transfer_fee = (int(amount/1000.0 - 0.001) + 1.0) * \
                                self.fee_table.loc[ticker,'transfer_fee_on_long']
                    
                commission_fee = max(amount * order_price * \
                                     self.fee_table.loc[ticker,'commission_fee_rate_long'],5.0) \
                                if self.fee_table.loc[ticker,'commission_fee_rate_long'] != 0 else 0
                                    
                transaction_fee = tax + transfer_fee + commission_fee                

                while cash < amount * order_price + transaction_fee:
                    # 此处采用部分成交机制
                    ## 找到最大可成交数量
                    amount -= self.fee_table.loc[ticker,'min_amount_long'] 
                    
                    if amount < self.fee_table.loc[ticker,'min_amount_long']:
                        break
                    
                    tax = abs(amount) * order_price * \
                        self.fee_table.loc[ticker,'tax_rate_long']
                    transfer_fee = (int(amount/1000.0 - 0.001) + 1.0) * \
                                    self.fee_table.loc[ticker,'transfer_fee_on_long']
                        
                    commission_fee = max(amount * order_price * \
                                         self.fee_table.loc[ticker,'commission_fee_rate_long'],5.0) \
                                    if self.fee_table.loc[ticker,'commission_fee_rate_long'] != 0 else 0
                                        
                    transaction_fee = tax + transfer_fee + commission_fee  
                
                if amount < self.fee_table.loc[ticker,'min_amount_long']:                        
                    order.order_state = ORDER_STATUS.REJECTED
                    reject_event = Event(EVENT.REJECT_ORDER,
                     reason = 'Not enough cash',
                     order = order)
                    self.env.event_bus.publish_event(reject_event)
                    continue
                
                else:
                    order.order_state = ORDER_STATUS.PARTIAL_FILLED
                    order.fill_dt = trading_dt
                    order.tax = tax
                    order.commission_fee = commission_fee
                    order.transfer_fee = transfer_fee
                    order.transaction_fee = transaction_fee
                    order.match_price = order_price
                    order.match_amount = amount                      
                    trade_event = Event(EVENT.TRADE,calendar_dt = calendar_dt,
                                       trading_dt = trading_dt,order = order)
                    self.env.event_bus.publish_event(trade_event)                         
                    continue
                
            elif direction == DIRECTION_SHORT:
                tax = abs(amount) * order_price * \
                    self.fee_table.loc[ticker,'tax_rate_short']
                transfer_fee = (int(amount/1000.0 - 0.001) + 1.0) * \
                                self.fee_table.loc[ticker,'transfer_fee_on_short']
                    
                commission_fee = max(amount * order_price * \
                                     self.fee_table.loc[ticker,'commission_fee_rate_short'],5.0) \
                                if self.fee_table.loc[ticker,'commission_fee_rate_short'] != 0 else 0
                transaction_fee = tax + transfer_fee + commission_fee
                
                position = self.env.account.get_position(ticker)
                
                if abs(amount) > position:
                    amount = - position
            
            # 市场检验
            high_price = self.env.bar_map.get_stock_latest_bar_value(ticker,'high_price')
            low_price = self.env.bar_map.get_stock_latest_bar_value(ticker,'low_price')
            total_amount = self.env.bar_map.get_stock_latest_bar_value(ticker,'volume')
            
            if order_price > high_price:
                order.order_state = ORDER_STATUS.REJECTED
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order price is too high',
                 order = order)
                self.env.event_bus.publish_event(reject_event)  
                continue
            if order_price < low_price:
                order.order_state = ORDER_STATUS.REJECTED
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order price is too low',
                 order = order)
                self.env.event_bus.publish_event(reject_event)
                continue
            if amount >= total_amount:
                order.order_state = ORDER_STATUS.REJECTED
                reject_event = Event(EVENT.REJECT_ORDER,
                 reason = 'order amount is too much',
                 order = order)
                self.env.event_bus.publish_event(reject_event) 
                continue
                
            # 订单成交
            order.order_state = ORDER_STATUS.FILLED
            order.fill_dt = trading_dt
            order.tax = tax
            order.commission_fee = commission_fee
            order.transfer_fee = transfer_fee
            order.transaction_fee = transaction_fee
            order.match_price = order_price    
            order.match_amount = amount
            
            trade_event = Event(EVENT.TRADE,calendar_dt = calendar_dt,
                               trading_dt = trading_dt,order = order)
            self.env.event_bus.publish_event(trade_event)                      
          
       
        
        
    