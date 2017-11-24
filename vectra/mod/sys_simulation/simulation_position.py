# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:46:23 2017

@author: ldh
"""

# position.py

import copy
import numpy as np

from vectra.constants import DIRECTION_LONG,DIRECTION_SHORT

class SimulationPosition():
    def __init__(self,universe):
        self.universe = np.array(universe)
        self.position = np.zeros(len(self.universe))
        self.position_available = np.zeros(len(self.universe))
        self.position_cost = np.zeros(len(self.universe))
        self.position_market_value = np.zeros(len(self.universe))
        
    #%% 更新函数
    def refresh_trade(self,fill_order):
        ticker = fill_order.ticker
        direction = fill_order.direction
        match_price = fill_order.match_price
        amount = fill_order.amount
        transaction_fee = fill_order.transaction_fee
        
        ind = np.where(self.universe == ticker)[0][0]
        
        if direction == DIRECTION_LONG:
            self.position_cost[ind] = (self.position_cost[ind] * self.position[ind] + \
                              amount * match_price) / (self.position[ind] + amount)
            self.position[ind] += amount
            self.position_market_value[ind] += amount * match_price
            money = -amount * match_price - transaction_fee
                        
        if direction == DIRECTION_SHORT:
            self.position_cost[ind] = (self.position_cost[ind] * self.position[ind] - \
                  amount * match_price) / (self.position[ind] + amount)
            self.position[ind] -= amount
            self.position_market_value[ind] -= amount * match_price 
            money = amount * match_price - transaction_fee       
        return money
    
    def refresh_post_bar(self,close_price):
        self.position_market_value = close_price * self.position
        self.total_account_value = self.position_market_value.sum()
    
    def refresh_settlement(self):
        self.position_available = copy.copy(self.position)
    
    #%% 查询
    @property
    def total_market_value(self):
        return self.position_market_value.sum()
                      
    def get_position(self,ticker):
        ind = np.where(self.universe == ticker)[0][0]
        return self.position[ind]    
    
    def get_position_cost(self,ticker):
        ind = np.where(self.universe == ticker)[0][0]
        return self.position_cost[ind]
    
    def get_market_value(self,ticker):
        ind = np.where(self.universe == ticker)[0][0]
        return self.position_market_value[ind]        
    
    #%% 持久化
    def get_state(self):
        state_data = {'universe':self.universe,
                      'position':self.position,
                      'position_available':self.position_available,
                      'position_cost':self.position_cost,
                      'position_market_value':self.position_market_value}
        return state_data
    
    def set_state(self,state):
        self.universe = state['universe']
        self.position = state['position']
        self.position_available = state['position_available']
        self.position_cost = state['position_cost']
        self.position_market_value = state['position_market_value']    


