# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:11:54 2017

@author: ldh
"""

# account.py
import pickle
from .simulation_position import SimulationPosition
from vectra.events import EVENT
from vectra.constants import HARD_MODE

class SimulationAccount():
    
    def __init__(self,env):
        
        self.env = env
        
        self.cash = env.capital
        self.position = SimulationPosition(self.env.universe)
        self.total_account_value = self.cash
            
        self.env.event_bus.add_listener(EVENT.TRADE,self._handle_fill_order)
        if self.env.data_mode == HARD_MODE:
            self.env.event_bus.add_listener(EVENT.PRE_BEFORE_TRADING,
                                            self._refresh_pre_before_trading)
        self.env.event_bus.add_listener(EVENT.POST_BAR,self._refresh_post_bar)
        self.env.event_bus.add_listener(EVENT.SETTLEMENT,self._refresh_settlement)
        
    #%% 监听函数
    def _handle_fill_order(self,event):
        '''
        接收成交时间。对仓位和成本进行调整。对市场价值和资产总值不做调整。
        '''
        fill_order = event.order
        money = self.position.refresh_trade(fill_order)
        self.cash += money
                    
    def _refresh_post_bar(self,event):
        '''
        bar后更新持仓市值.
        '''
        close_price = self.env.bar_map.get_latest_bar_value()
        self.position.refresh_post_bar(close_price)
        market_value = self.position.total_market_value
        self.total_account_value = self.cash + market_value

        
    def _refresh_settlement(self,event):
        '''
        更新可卖证券。
        '''
        self.position.refresh_settlement()
        
    #%% 查询函数
    @property
    def cash(self):
        return self.cash
    
    @property
    def market_value(self):
        return self.position.total_market_value
    
    @property
    def total_account_value(self):
        return self.total_account_value
    
    def get_position(self,ticker):
        return self.position.get_position(ticker) 
    
    def get_position_cost(self,ticker):
        return self.position.get_position_cost(ticker)
    
    def get_market_value(self,ticker):
        return self.position.get_market_value(ticker)
    
    #%% 持久化
    def get_state(self):
        state_data = {'cash':self.cash,
                      'total_account_value':self.total_account_value,
                      'position':self.position.get_state()}
        state_data = pickle.dumps(state_data)
        return state_data
            
    def set_state(self,state):
        state = pickle.loads(state)
        self.cash = state['cash']
        self.total_account_value = state['total_account_value']
        self.position.set_state(state['position'])
      
            
        
        
            
        
        
        
        