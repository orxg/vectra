# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 10:52:37 2018

@author: ldh
"""

# run_weight_backtest_template.py
#%% 0. Basic settings
strategy_name = ''
start_date = ''
end_date = ''
initial_capital = 10000
data_path = ''
weight_path = ''
report_path = ''
universe = []

# Options
report_dir = ''
#%% 1. Prepare data
'''
Prepare your data here.
'''
data_path = ''

#%% 2. Generate weight history
'''
Generate your weight history here.
AND SAVE IT TO report_path.
'''

#%% 3. Backtest
from vectra import run_weight

config = \
{'base':
    {'start_date':start_date,
     'end_date':end_date,
     'capital':initial_capital,
     'frequency':'1d',
     'universe':universe},
'source':'excel',
'file_path':data_path,
'fee':{}}
        
report = run_weight(config,strategy_name,weight_path,report_path)

#%% 4. Get detail report
import os
from vectra.utils.analyse.analyse import plot,visualize_report
os.mkdir(report_dir)
visualize_report(report,save_path = report_dir)
plot(report,save_path = os.path.join(report_dir,'value.png'))



