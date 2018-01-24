# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 08:33:34 2017

@author: ldh
"""

# run_strategy.py

config = {'base':
    {'start_date':'20160120',
     'end_date':'20170201',
     'frequency':'1d',
     'capital':100000,
     'universe':['600340','600066','600660']},
     'source':'sql',
     'file_path':''}

from vectra import run_file

strategy_path = './test/test_moving_average.py'
report = run_file(config,'test_buy_and_hold',strategy_path,report_path = 'G:\\Work_ldh\\PM\\F1\\bt')



