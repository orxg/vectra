# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:21:01 2018

@author: ldh
"""

# easy_api.py

def get_config(universe,start_date,end_date,
               capital = 1000000.0,frequency = '1d',
               source = 'excel',file_path = ''):
    '''
    制造config字典方法。
    
    Parameters
    ----------
    universe
        证券池
    start_date
        '20140101'
    end_date
        '20150601'
    capital
        float,初始资金
    frequency
        '1d'
    source
        数据源类型,sql或excel,默认为sql
    file_path
        excel数据源下的数据地址
        
    Returns
    --------
    Dict: 用户config
    '''
    easy_config = {'base':
        {'start_date':start_date,
         'end_date':end_date,
         'capital':capital,
         'frequency':frequency,
         'universe':universe},
    	 'source':source,
    	 'file_path':file_path}
    return easy_config