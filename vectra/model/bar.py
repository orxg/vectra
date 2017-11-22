# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:56:35 2017

@author: ldh
"""

# bar.py

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
        data_proxy = self.env.data_proxy
        bar = data_proxy.get_bar()
        self._data.append(bar)
        self._current_data.append(bar)
            
    def _clear_post_settlement(self,event):
        self._current_data = []
        
    #%% api
    def __getitem__(self,ticker):
        return self._data[ticker]
            
    def get_latest_bar(self):      
        return self._data[-1]
    
    def get_latest_bars(self,n):
        return self._data[-n:]
    
    def get_latest_bar_value(self,val_type = 'close_price'):
        '''
        获取最近的bar的某个属性值。
        '''
        return self._data[-1][val_type]    
    
    def get_stock_latest_bar_value(self,ticker,val_type = 'close_price'):
        '''
        获取最近的某只股票的bar的某个属性值。
        '''
        num = self.universe.index(ticker)
        return self._data[-1][val_type][num]
    
    def get_current_day_bar(self,style = 1):
        '''
        获取当日的所有可得bar.主要用于分钟级策略.
        
        Parameters
        ----------
        style
            返回数据的格式。
            1为根据属性返回。默认为1.
            2为根据股票代码返回。
        Returns
        ---------
        dict
            index
                 pd.Timestamp
            columns
                (open_price,high_price,low_price,close_price,volume,amount)
        '''
        current_data = self._current_data
        if style == 1:
            universe = current_data[-1]['universe']
            date_time = [i['date_time'] for i in current_data]
            open_price = [i['open_price'] for i in current_data]
            high_price = [i['high_price'] for i in current_data]
            low_price = [i['low_price'] for i in current_data]
            close_price = [i['close_price'] for i in current_data]
            volume = [i['volume'] for i in current_data]
            amount = [i['amount'] for i in current_data]
            
            return {'universe':universe,
                    'date_time':date_time,
                    'open_price':open_price,
                    'high_price':high_price,
                    'low_price':low_price,
                    'close_price':close_price,
                    'volume':volume,
                    'amount':amount}
            
        elif style == 2:
            pass
        return current_data
        
                
         
        
    

