# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:04:01 2017

@author: ldh
"""

# dynamic_universe.py

from ..events import EVENT
from ..environment import Environment

class DynamicUniverse():
    
    def __init__(self):
        env = Environment.get_instance()
        self.universe = env.universe
        self.start_date = env.start_date
        self.end_date = env.end_date
        self.dynamic_universe = []        
        self.trade_status = env.data_proxy.get_trade_status(self.universe,
                                                             self.start_date,
                                                             self.end_date)
        env.event_bus.add_listener(EVENT.PRE_BEFORE_TRADING,self._refresh_pre_before_trading)
        
    def _refresh_pre_before_trading(self,event):
        self.dynamic_universe = []
        env = Environment.get_instance()
        for ticker in self.universe:
            if env.data_proxy.if_tradable(ticker,env.calendar_dt):
                self.dynamic_universe.append(ticker)
                
    def get_dynamic_universe(self):
        return self.dynamic_universe
        

