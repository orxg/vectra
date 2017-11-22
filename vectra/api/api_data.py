# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 08:43:43 2017

@author: ldh

定义关于数据的api.
"""

# api_data.py

from VectorTrader.data.data_source.mixed_data_source.mixed_data_source import MixedDataSource

mixed_data_source = MixedDataSource()

def get_symbols(symbol):
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
    return mixed_data_source.get_symbols(symbol)

def get_history(ticker,start_date,end_date,frequency,kind):
    '''
    数据接口。
    数据根据上证交易日进行了补全，没有数据用空值表示。
		
    Parameters
    -----------
		start_date
			'20100101'
		end_date
			'20150101'
		frequency 
			'1d','1m','5m'
		kind
			'0' 不复权
			'1' 后复权
			'-1' 前复权
            
    Returns
    --------
		DataFrame (date_time,open_price,high_price,low_price,close_price,volume,amount)
    '''
    return mixed_data_source.get_history(ticker,start_date,end_date,frequency,kind)

def get_stocks_basics(ticker_list):
    '''
    获取股票基本信息。包括其所属行业，行业指数代码。
    '''
    return mixed_data_source.get_stocks_basics(ticker_list)



def get_stock_factors(ticker, field, start_date, end_date,other):
    '''
    获取股票因子数据。
    仅获得交易日数据。
    
    Parameters
    -----------
    ticker
        股票代码,'600340'
    field
        所取字段 ['pe_ttm','pb_lf']
    start_date
        开始日期，交易日日期, 20160104，若非交易日无法取到数据
    end_date
        结束日期
    other
        其他信息
    Returns
    --------
    DataFrame
        index:DatetimeIndex
        columns:field_1,field_2,....,field_n,ticker
    
    Notes
    ------
    估值类因子
        'pe_ttm'
            市盈率TTM
        'pb_mrq'
            市净率MRQ(most recent quarter)
        'pb_lf'
            市净率LF(last file)
        'ps_ttm'
            市销率TTM
        'pcf_ocf_ttm'
            市现率TTM(经营现金流)                    
    '''
    return mixed_data_source.get_stock_factors(ticker,field,
                                               start_date, end_date,other)

def get_stock_factors_on_year(ticker,field,trade_date,year):
    '''
    根据年份获取领先预测数据。
    
    Parameters
    ------------
    ticker
        '600340'
    field
        ['west_mediansales']
    trade_date
        '20170908',预测提出时间
    year
        '2018',预测年份
    Retruns
    --------
    DataFrame
        index: datetime
        columns: field1,field2,...,ticker,year
    '''
    return mixed_data_source.get_stock_factors_on_year(ticker,field,trade_date,year)

def get_industry_factors(industry_wind_id, field, start_date, end_date):
    '''
    获取万得行业指数数据。
    
    Parameters
    -----------
    indusry_wind_id
        万得行业指数代码,'882100.WI'
    field
        所取字段 ['pe_ttm','pb_lf']
    start_date
        开始日期，交易日日期, 20160104，若非交易日无法取到数据
    end_date
        结束日期
    add_industry_id
        是否添加行业代码作为左后一列
    Returns
    --------
    DataFrame
        columns:wind_id,field_1,field_2,....,field_n,industry_wind_id
    
    Notes
    ------
    估值类因子
        'pe_ttm'
            市盈率TTM
        'pb_mrq'
            市净率MRQ(most recent quarter)
        'pb_lf'
            市净率LF(last file)
        'ps_ttm'
            市销率TTM
        'pcf_ocf_ttm'
            市现率TTM(经营现金流)
                    
    '''
    return mixed_data_source.get_industry_factors(industry_wind_id,field,
                                                  start_date, end_date) 
    
def get_stock_factors_with_industry(ticker,field,start_date,end_date):
    '''
    获取股票因子数据,以及对应的行业因子数据。目前支持二级行业。
    
    Returns
    --------
    DataFrame
        columns
            field_1,field_2,...,field_n,ticker,industry_field_1,...,industry_field_n,industry_wind_id
    '''
    return mixed_data_source.get_stock_factors_with_industry(ticker,field,
                                                             start_date,end_date)
    
def get_stocks_factors(universe,factors,trade_date):
    '''
    获取多只股票的多个因子,仅支持单一交易日。
    
    Parameters
    -----------
    universe
        ['600340','000001']
    factors
        ['ev','pe_ttm']
    trade_date
        '20150103'

    Returns
    --------
    DataFrame
        index [ticker,...]
        columns factor1,factor2,...
    '''
    return mixed_data_source.get_stocks_factors(universe,factors,trade_date)    
