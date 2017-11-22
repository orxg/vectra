# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:12:48 2017

@author: ldh
"""

# data_proxy.py
import datetime

from ..constants import (EASY_MODE,HARD_MODE,
                         BACKTEST,PAPER_TRADING)
from ..environment import Environment
from ..events import EVENT
from ..utils.convertor import array_2_generator

class DataProxy():
    '''
    对不同类型的data_source的封装。计划支持不同模式下的代理。
    对于回测/模拟/实盘实现一套系统内部的数据结构，并定义接口。
    对于研究而言，实现以DataFrame为基准的数据结构的接口。
    
    这样的好处在于DataSource只需要实现DataFrame数据类型。
    DataProxy负责对DataFrame数据类型进行加工得到定义的数据类型。
        
    20170926
    ---------
        向量化获取数据、向量化底层处理。
        
    20170901
    ---------
        采用不复权数据进行回测。        
    20170828
    ---------
        将回测数据一次性转换成bar_list,并构造成生成器。这样，
        在每次post bar后生成当前bar对象,bar_map通过get_bar方法取得对应的bar.        
    20170825
    ----------
        创建MixedDataSource集成所有可得数据源。作为默认数据源。
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
        self._date_time = array_2_generator(self._backtest_data['date_time'])
        self._open_price = array_2_generator(self._backtest_data['open_price'])
        self._high_price = array_2_generator(self._backtest_data['high_price'])
        self._low_price = array_2_generator(self._backtest_data['low_price'])
        self._close_price = array_2_generator(self._backtest_data['close_price'])        
        self._volume = array_2_generator(self._backtest_data['volume'])
        self._amount = array_2_generator(self._backtest_data['amount'])
                
        self._trade_status = self.get_trade_status()

            
    #%% 回测内部api
    def get_bar(self):
        '''
        返回按照属性分类的bar,是一个字典
        
        Returns
        --------
        dict
            含有各个属性的字典  
       
        '''
        if self.mode == BACKTEST:
            date_time = next(self._date_time)[0]
            open_price = next(self._open_price)
            high_price = next(self._high_price)
            low_price = next(self._low_price)
            close_price = next(self._close_price)
            volume = next(self._volume)
            amount = next(self._amount)
            
            bar = {'date_time':date_time,
                   'universe':self._universe,
                   'open_price':open_price,
                   'high_price':high_price,
                   'low_price':low_price,
                   'close_price':close_price,
                   'volume':volume,
                   'amount':amount}
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
                date_time,open_price,high_price,low_price,close_price,volume,amount 
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
                date_time
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
        return self.data_source.get_trade_status(universe,start_date,end_date)  

    def if_tradable(self,ticker,date):
        '''
        判断当前标的在date日是否可以交易。
        '''
        trade_status = self._trade_status.ix[date,ticker]
        if trade_status:
            return True
        else:
            return False
#%%                             Abandon temporarily

#==============================================================================
#         self._dividend_data = {}
#         self._rights_issue_data = {}
#         self._trade_status_data = {}
#         self._list_delist_date_data = {}
#         self._calendar_days = self.get_calendar_days(start_date,end_date) 
#         
#         for ticker in universe:
#             self._dividend_data[ticker] = self.get_dividend(ticker,
#                                start_date,end_date)
#             self._rights_issue_data[ticker] = self.get_rights_issue(ticker,
#                                    start_date,end_date)
#             self._trade_status_data[ticker] = self.get_trade_status(ticker,
#                                    start_date,end_date)
#             self._list_delist_date_data[ticker] = self.get_list_delist_date(ticker)
#==============================================================================         
#==============================================================================
#     def get_history(self,universe,start_date,end_date,frequency,kind):
#         '''
#         数据接口。
#         数据根据上证交易日进行了补全，没有数据用空值表示。
# 		
#         Parameters
#         -----------
#         ticker
#             '600340'
#     		start_date
#     			'20100101'
#     		end_date
#     			'20150101'
#     		frequency 
#     			'1d','1m','5m'
#     		kind
#     			'0' 不复权
#     			'1' 后复权
#     			'-1' 前复权
#                 
#         Returns
#         --------
#     		DataFrame (date_time,open_price,high_price,low_price,close_price,volume,amount)
#         '''
#         return self.data_source.get_history(universe,start_date,end_date,frequency,kind)
#==============================================================================
            


#==============================================================================
#     def get_rights_issue(self,ticker,start_date,end_date):
#         '''
#         获取股票已实施配股数据。若时间段内股票没有配股则返回空表。
# 		
#         Parameters
#         ----------
#     		ticker
#     			'600340'
#     		start_date
#     			'20100101'
#     		end_date
#     			'20150101'
#         Returns
#         --------
#     		DataFrame
#     			index ex_rights_date
#     			columns 
#     				'ex_rights_date','rights_issue_per_stock','rights_issue_price',
#     				'transfer_rights_issue_per_stock','transfer_price'
#     					(除权日,每股配股,配股价，每股转配，每股转配价)
#         '''
#         return self.data_source.get_rights_issue(ticker,start_date,end_date)
#     
#     def get_dividend(self,ticker,start_date,end_date):
#         '''
#         获取股票时间段内实施的分红送股转增数据。若时间段内股票没有分红送股则返回空表。
# 		
#         Parameters
#         ----------
#     		ticker
#     			'600340'
#     		start_date
#     			'20100101'
#     		end_date
#     			'20150101'
#         Returns
#         --------
#     		DataFrame
#     			index XD_date
#     			columns XD_date,dividend_per_share,multiplier
#     					(除权除息日,每股分红,分红后每股乘数)
#         '''
#         return self.data_source.get_dividend(ticker,start_date,end_date)
#     
#==============================================================================

    
#==============================================================================
#     def get_suspends(self,trade_date):
#         '''
#         停牌股票。
#         
#         Parameters
#         -----------
#         trade_date
#             '20150101'
#         Returns
#         ---------
#         list 
#             [ticker,...]
#         '''
#         return self.data_source.get_suspends(trade_date)  
#     
#     def get_list_delist_date(self,ticker):
#         '''
#         获取股票上市与退市日期。若没有退市，则退市为0.
# 		
#         Parameters
#         -----------
#     		ticker
#     			600340
#         Returns
#         --------
#     		tuple
#     			(list_date,delist_date) datetime类型
#                 
#         '''
#         return self.data_source.get_list_delist_date(ticker)
#==============================================================================
    
#==============================================================================
#     def get_pre_before_trading_dividend(self,ticker,dt):
#         if self.mode == BACKTEST:
#             try:
#                 return self._dividend_data[ticker].loc[dt]
#             except:
#                 return 0
#         elif self.mode == PAPER_TRADING:
#             try:
#                 if isinstance(dt,datetime.datetime):
#                     dt_ = dt.strftime('%Y%m%d')
#                 return self.get_dividend(ticker,dt_,dt_).loc[dt]
#             except:
#                 return 0
#     
#     def get_pre_before_trading_rights_issue(self,ticker,dt):
#         if self.mode == BACKTEST:
#             try:
#                 return self._rights_issue_data[ticker].loc[dt]
#             except:
#                 return 0
#         elif self.mode == PAPER_TRADING:
#             try:
#                 if isinstance(dt,datetime.datetime):
#                     dt_ = dt.strftime('%Y%m%d')
#                 return self.get_rights_issue(ticker,dt_,dt_).loc[dt]
#             except:
#                 return 0
#     
#     def is_date_trade(self,ticker,dt):
#         if self.mode == BACKTEST:
#             list_date,delist_date = self._list_delist_date_data[ticker]
#             if delist_date != 0:
#                 if dt >= list_date and dt < delist_date:
#                     if self._trade_status_data[ticker].loc[dt,'status'] == 1:
#                         return True
#                 else:
#                     return False
#             elif delist_date == 0:
#                 if dt >= list_date:
#                     if self._trade_status_data[ticker].loc[dt,'status'] == 1:
#                         return True
#                     else:
#                         return False
#         
#         elif self.mode == PAPER_TRADING:
#             try:
#                 list_date,delist_date = self.get_list_delist_date(ticker)
#                 if delist_date != 0:
#                     if dt >= list_date and dt < delist_date:
#                         if not ticker in self.current_suspends:
#                             return True
#                     else:
#                         return False
#                 elif delist_date == 0:
#                     if dt >= list_date:
#                         if not ticker in self.current_suspends:
#                             return True
#                         else:
#                             return False      
#             except:
#                 return True
#==============================================================================
    