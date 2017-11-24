# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:32:09 2017

@author: ldh
"""

# interface.py
from abc import ABCMeta,abstractmethod

class AbstractDataSource():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_attr(self,universe,start_date,end_date,frequency,data_mode):
        '''
        按属性获取时间、高、开、低、收、成交量、成交金额数据。
        
        Parameters
        -----------
        universe
            list,股票池 ['600340','000001']
        start_date
            '20100101'
        end_date
            '20150101'
        frequency
            '1d','1m','3m',...
        data_mode
            EASY_MODE,HARD_MODE

        Returns
        --------
        dict
            keys : 
                trade_date,open_price,high_price,low_price,close_price,amount,volume
            value : 
                np.array
                
        Notes
        ------
        数据按列对应universe
        '''
        raise NotImplementedError
        
    @abstractmethod
    def get_calendar_days(self,start_date,end_date):
        '''
        返回start_date到end_date间的交易日。
		
        Parameters
        -----------
    		start_date
        		'20100101'
    		end_date
        		'20150101'
                
        Returns
        -------
    		list 
            [datetime]
        '''
        raise NotImplementedError
		
    @abstractmethod	
    def get_trade_status(self,universe,start_date,end_date):
        '''
        获取股票交易状态。
		
        Parameters
        -----------
        universe
            stocks
        start_date
            '20100101'
        end_date
            '20150101'
                
        Returns
        --------
        DataFrame 
            index 
                datetime,'trade_date'
            columns
                (ticker1,ticker2,...,tickern)
            values
                [[0,1,1,1],[0,0,0,0]]
        Notes
        -------
        status 
        正常交易: 1
        停牌或未上市或已退市: 0
        '''
        raise NotImplementedError
		
class AbstractMod():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def start_up(self,env):
        raise NotImplementedError
        
    def tear_down(self):
        raise NotImplementedError
        
        