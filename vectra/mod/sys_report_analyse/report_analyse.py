# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:30:39 2017

@author: ldh
"""

# report_analyse.py

import numpy as np
import pandas as pd
from vectra.utils.analyse.analyse import plot,plot_history_weight
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

class ReportAnalyser():
    def __init__(self):
        pass
    
    def plot(self,report):
        '''
        根据报告做图.
        '''
        # 资产收益率曲线
        plot(report)
#        portfolio_return = pd.DataFrame(report['portfolio_value'],
#                                        columns = ['calendar_dt',
#                                                   'trading_dt',
#                                                   'portfolio_value'])
#        portfolio_return['portfolio_accumulate_return'] = \
#        portfolio_return['portfolio_value'] / portfolio_return['portfolio_value'].values[0] - 1.0
#        portfolio_return = portfolio_return[['calendar_dt','portfolio_accumulate_return']]
#        
#        x_vals = portfolio_return['calendar_dt'].values
#        y_vals = portfolio_return['portfolio_accumulate_return'].values
#        N = len(x_vals)
#        ind = np.arange(N)
#        
#        def format_date(x,pos=None):
#            this_ind = np.clip(int(x+0.5),0,N-1)
#            return pd.to_datetime(x_vals[this_ind]).strftime('%Y-%m-%d')
#        
#        fig,ax = plt.subplots(figsize = (20,8))
#        ax.plot(ind,y_vals)
#        ax.xaxis.set_major_formatter(FuncFormatter(format_date))
#        ax.set_yticklabels(['{:.2%}'.format(y) for y in ax.get_yticks()])
#        ax.grid(True)
#        ax.set_title('Strategy Accumulate Return',fontsize = 25)
#        ax.set_xlabel('Date',fontsize = 20)
#        ax.set_ylabel('Accumulate Return',fontsize = 20)
#        plt.show()
        
    def plot_history_weight(self,report):
        plot_history_weight(report)
        
        
