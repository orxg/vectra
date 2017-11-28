# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:18:32 2017

@author: ldh
"""

# context.py
import six
import pickle

from ..environment import Environment

class Context():
    '''
    用户策略上下文         
    '''
    def __init__(self):
        self.signal_post_before_trading = None # 盘前信息
        self.signal_post_after_trading = None # 盘后信息
      
    #%% 持久化
    def get_state(self):
        state_data = {}
        for key,value in six.iteritems(self.__dict__):
            if key.startswith('_'):
                continue
            try:
                state_data[key] = pickle.dumps(value)
            except:
                print '{} can not be pickled'.format(key)
        return pickle.dumps(state_data)
            
    def set_state(self,state):
        state_data = pickle.loads(state)
        for key,value in six.iteritems(state_data):
            try:
                self.__dict__[key] = pickle.loads(value)
            except:
                print '{} can not be loaded'.format(key)
         
    #%% 查询  
    @property
    def dynamic_universe(self):
        return Environment.get_instance().get_dynamic_universe()
    
    @property
    def universe(self):
        return Environment.get_instance().get_universe()
    
    @property
    def current_date(self):
        return Environment.get_instance().calendar_dt
    
    @property
    def account(self):
        return Environment.get_instance().account
    
    #%% 暂不支持 
    @property
    def active_order(self):
        '''
        当日待成交订单.
        '''
        pass
    
    @property
    def trade_order(self):
        '''
        当日已成交订单.
        '''
        pass
    
    @property
    def killed_order(self):
        '''
        当日已撤订单.
        '''
        pass

    
    
    
    
    
