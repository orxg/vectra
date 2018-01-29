# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:56:35 2017

@author: ldh
"""

# bar.py
import logging
import pandas as pd

from ..events import EVENT

class BarMap():
    
    #%% 初始化
    def __init__(self,env):
        '''
        为Strategy,Account,Broker提供bar数据。
        是系统内部数据的传递者,其数据来自于data_proxy.
        '''
        self._data = []
        self._current_data = []
        self.env = env 
        self.universe = self.env.universe
        self.env.event_bus.add_listener(EVENT.PRE_BAR,self._update_pre_bar)
        self.env.event_bus.add_listener(EVENT.POST_SETTLEMENT,
                                        self._clear_post_settlement)
        
    def __str__(self):
        return 'A data structure used as the router.'
    
    __repr__ = __str__
 
    #%% 监听函数
    def _update_pre_bar(self,event):
        logging.info('UPDATE_PRE_BAR WHEN %s'%(self.env.calendar_dt))
        data_proxy = self.env.data_proxy
        bar = data_proxy.get_bar()
        self._data.append(bar)
        self._current_data.append(bar)
            
    def _clear_post_settlement(self,event):
        self._current_data = []
        
    #%% 内部api
    def __getitem__(self,ticker):
        return self._data[ticker]
            
    def get_latest_bar(self):      
        return self._data[-1]
    
    def get_latest_bars(self,n):
        return self._data[-n:]
    
    def get_latest_bar_value(self,val_type = 'close_price'):
        '''
        获取最近的bar的某个属性值。
        
        Parameters
        -----------
        val_type
            bar类型,open_price,high_price,low_price,close_price,volume,amount
        
        Returns
        -------
        narray
        '''
        return self._data[-1][val_type]    
    
    def get_stock_latest_bar_value(self,ticker,val_type = 'close_price'):
        '''
        获取最近的bar的某个属性值。
        
        Parameters
        -----------
        ticker
            str,标的代码
        val_type
            bar类型,open_price,high_price,low_price,close_price,volume,amount
        
        Returns
        -------
        float-like
        '''
        num = self.universe.index(ticker)
        return self._data[-1][val_type][num]
    
    #%% 外部api,查询函数,用户使用
    def get_history(self,attr,n):
        '''
        用户提取属性数据接口。
        
        Parameters
        ----------
        attr
            提取属性
            open_price,high_price,low_price,close_price,amount,volume
        n
            提取数量
            
        Notes
        -----
        为了避免未来函数,该接口不能获取当日的bar.
        '''
        data = self._data[-n-1:-1]
        if len(data) != 0:
            trade_date = [_['trade_date'] for _ in data]
            data_attr = [_[attr] for _ in data]
            df = pd.DataFrame(data_attr,index = trade_date,columns = self.universe)     
            return df
        else:
            return None
        
                
         
        
    

