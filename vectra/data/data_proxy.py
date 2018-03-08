# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:12:48 2017

@author: ldh
"""

# data_proxy.py

import logging

from ..constants import BACKTEST
from ..environment import Environment
from ..utils.convertor import array_2_generator

class DataProxy():
    '''
    对不同类型的data_source的封装。计划支持不同模式下的代理。
    对于回测/模拟/实盘实现一套系统内部的数据结构，并定义接口。
    对于研究而言，实现以DataFrame为基准的数据结构的接口。
    '''
    #%% 初始化data_proxy对象
    def __init__(self,data_source,data_mode,mode):
        '''
        初始化data_proxy.
        
        Parameters
        ------------
        data_source
            数据源对象,提供能data_proxy所需的api(必须实现):
                get_attr,get_calendar_days,get_trade_status,get_symbols
        data_mode
            数据模式常量,复权与不复权两种
        mode
            模式常量,回测与模拟    
        '''
        self.data_source = data_source 
        self.data_mode = data_mode
        self.mode = mode
        
        if self.mode == BACKTEST:
            self._initilize_backtest_data()
            
    def _initilize_backtest_data(self):
        '''
        准备回测所需数据.
        '''        
        env = Environment.get_instance()
        universe = env.universe
        start_date = env.start_date
        end_date = env.end_date
        frequency = env.frequency

        # 回测数据
        
        self._universe = universe
        self._backtest_data = self.get_attr(self._universe,start_date,end_date,
                                            frequency,self.data_mode)
        self._trade_date = array_2_generator(self._backtest_data['trade_date'])
        self._open_price = array_2_generator(self._backtest_data['open_price'])
        self._high_price = array_2_generator(self._backtest_data['high_price'])
        self._low_price = array_2_generator(self._backtest_data['low_price'])
        self._close_price = array_2_generator(self._backtest_data['close_price'])        
        self._volume = array_2_generator(self._backtest_data['volume'])
        self._amount = array_2_generator(self._backtest_data['amount'])
                
        self._trade_status = self.data_source.get_trade_status(universe,start_date,end_date)

            
    #%% 回测内部api
    def get_bar(self):
        '''
        返回按照属性分类的bar,是一个字典
        
        Returns
        --------
        dict
            含有各个属性的字典  
       
        '''
        env = Environment.get_instance()
        if self.mode == BACKTEST:
            trade_date = next(self._trade_date)
            open_price = next(self._open_price)
            high_price = next(self._high_price)
            low_price = next(self._low_price)
            close_price = next(self._close_price)
            volume = next(self._volume)
            amount = next(self._amount)
            
            bar = {'trade_date':trade_date,
                   'universe':self._universe,
                   'open_price':open_price,
                   'high_price':high_price,
                   'low_price':low_price,
                   'close_price':close_price,
                   'volume':volume,
                   'amount':amount}
            logging.info('THIS IS A CALL FOR GET_BAR() WHEN %s'%(env.calendar_dt) + \
                         'THE DATA DATE IS %s'%(trade_date))
            return bar
        
        
    #%% 内部api
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
        return self.data_source.get_attr(universe,start_date,end_date,frequency,data_mode)

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
        if self.mode == BACKTEST:
            return self.data_source.get_calendar_days(start_date,end_date)
        
    def get_symbols(self,symbol):
        '''
        获取**当前**全A、指定板块、指数、ST的成分股代码。
        
        Parameters
        -----------
        symbol 
            获取类型
        Returns
        ----------
        list 
            [ticker,...]
        Notes
        ---------
        'A' 
            全A股
        'st' 
            st股票
        'hs300' 
            沪深300成分股
        'cyb' 
            创业板成分股
        'sz50' 
            上证50成分股
        'A-st' 
            剔除st股票后的全A股
        
        '''
        try:
            return self.data_source.get_symbols(symbol)
        except Exception as e:
            print e
            print 'data_source\'s method [get_symbols] is not realized correctly'
            raise    
            
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
        return self._trade_status

    def if_tradable(self,ticker,date):
        '''
        判断当前标的在date日是否可以交易。
        '''
        trade_status = self._trade_status.ix[date,ticker]
        if trade_status:
            return True
        else:
            return False
