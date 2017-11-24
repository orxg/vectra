# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 08:33:34 2017

@author: ldh
"""

# run_strategy.py

config = {'base':
    {'start_date':'20160103',
     'end_date':'20170201',
     'frequency':'1d',
     'capital':100000,
     'universe':['600340']}}

from vectra import run_file

strategy_path = './test/test_buy_and_hold.py'
#==============================================================================
# with open(strategy_path,'r') as f:
#     con = f.readlines()
#     for each in con:
#         print each
#==============================================================================
report = run_file(config,'test_buy_and_hold',strategy_path)



