# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:27:13 2017

@author: ldh
"""

# environment.py
from events import EventBus

class Environment():
    _env = None
    
    def __init__(self,config):
        '''
        
        Parameters
        -----------
        config
            Config对象
        '''
        Environment._env = self
        
        # 基础设定
        self.config = config 
        self._parse_config()
        
        # 数据源与数据代理
        self.data_source = None
        self.data_proxy = None
        
        # 事件源与监听函数列表
        self.event_bus = EventBus()
        self.event_source = None
    
        # 环境日期
        self.calendar = None
        self.calendar_dt = None
        self.trading_dt = None
        
        # 动态股票池
        self.dynamic_universe = None 
     
    def _parse_config(self):
        self.start_date = self.config.start_date
        self.end_date = self.config.end_date
        self.capital = self.config.capital
        self.universe = self.config.universe
        self.frequency = self.config.frequency
    
    @classmethod
    def get_instance(cls):
        return Environment._env
    
    #%% 数据源与数据代理
    def set_data_source(self,data_source):
        self.data_source = data_source
    
    def set_data_proxy(self,data_proxy):
        self.data_proxy = data_proxy   
    
    #%% 事件源
    def set_event_source(self,event_source):
        self.event_source = event_source
        
    #%% 日期
    def set_calendar(self,calendar):
        self.calendar = calendar
        
    #%% 组件
    def set_account(self,account):
        self.account = account
        
    def set_analyser(self,analyser):
        self.analyser = analyser
        
    def set_broker(self,broker):
        self.broker = broker
            
    def set_bar_map(self,bar_map):
        self.bar_map = bar_map
        
    def set_dynamic_universe(self,dynamic_universe):
        self.dynamic_universe = dynamic_universe    
        
    def set_context(self,context):
        self.context = context
    #%% 查询
    def get_dynamic_universe(self):
        return self.dynamic_universe.get_dynamic_universe()
    
    def get_universe(self):
        return self.universe
    