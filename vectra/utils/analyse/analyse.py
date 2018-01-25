# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:22:51 2018

@author: ldh
"""

# analyse.py
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def load_report(file_path):
    '''
    读取报告.
    '''
    with open(file_path,'r') as f:
        report = pickle.load(f)
    return report

def plot(report):
    '''
    根据报告做图.
    '''
    # 资产收益率曲线
    portfolio_return = pd.DataFrame(report['portfolio_value'],
                                    columns = ['calendar_dt',
                                               'trading_dt',
                                               'portfolio_value'])
    portfolio_return['portfolio_accumulate_return'] = \
    portfolio_return['portfolio_value'] / portfolio_return['portfolio_value'].values[0] - 1.0
    portfolio_return = portfolio_return[['calendar_dt','portfolio_accumulate_return']]
    
    x_vals = portfolio_return['calendar_dt'].values
    y_vals = portfolio_return['portfolio_accumulate_return'].values
    N = len(x_vals)
    ind = np.arange(N)
    
    def format_date(x,pos=None):
        this_ind = np.clip(int(x+0.5),0,N-1)
        return pd.to_datetime(x_vals[this_ind]).strftime('%Y-%m-%d')
    
    fig,ax = plt.subplots(figsize = (20,8))
    ax.plot(ind,y_vals)
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_yticklabels(['{:.2%}'.format(y) for y in ax.get_yticks()])
    ax.grid(True)
    ax.set_title('Strategy Accumulate Return',fontsize = 25)
    ax.set_xlabel('Date',fontsize = 20)
    ax.set_ylabel('Accumulate Return',fontsize = 20)
    plt.show()
    
def visualize_report(report,save_path):
    '''
    输出并保存可视化的报告.
    
    Parameters
    -----------
    report
        dict,vectra返回的report
    save_path
        str,回测细节记录保存地址
        
    Returns
    --------
    Tuple 结果DataFrame
    '''
    # 持仓记录
    holding_record = pd.DataFrame(np.array(report['position'])[:,2].tolist(),
                                  columns = report['universe'],
                                  index = np.array(report['position'])[:,0])
    # 持仓比例
    weight_record = pd.DataFrame()
    for record in report['daily_weight']:
        tmp_ser = record[2]
        tmp_ser.name = record[0]
        weight_record = pd.concat([weight_record,tmp_ser],axis = 1)
    weight_record = weight_record.T
    # 下单记录
    order_record = pd.DataFrame.from_records(report['history_orders'])
    # 成交记录
    fill_order_record = pd.DataFrame.from_records(report['history_fill_orders'])
    # 拒单记录
    reject_order_record = pd.DataFrame.from_records(report['history_rejected_orders'])
    
    # 保存
    holding_record.to_excel(os.path.join(save_path,'holding_record.xlsx'))
    order_record.to_excel(os.path.join(save_path,'order_record.xlsx'))
    fill_order_record.to_excel(os.path.join(save_path,'fill_order_record.xlsx'))
    reject_order_record.to_excel(os.path.join(save_path,'reject_order_record.xlsx'))
    
    # 返回
    return holding_record,order_record,fill_order_record,reject_order_record

def describe(report):
    '''
    根据报告做统计描述.
    '''
    # 累计收益率
    ini_value = report['daily_portfolio_value'][0][2]
    last_value = report['daily_portfolio_value'][-1][2]
    total_ret = (last_value - ini_value) / ini_value
    
    # 年化收益率
    start_date = report['daily_portfolio_value'][0][0]
    end_date = report['daily_portfolio_value'][-1][0]
    duration = end_date - start_date
    duration_days = duration.days
    annual_ret = (1 + total_ret) * 365.0 / duration_days
    
    # 交易次数
    # 根据fill_order数量来进行计算
    trade_times = len(report['history_fill_orders'])
    
    # 交易胜率
    
    # 最大回撤比率
    
    # 最大连盈周数
    pass

if __name__ == '__main__':
    file_path = 'G:\\Work_ldh\\PM\\F1\\bt\\fof_f1_2.pkl'
    report = load_report(file_path)
    plot(report)
    a = describe(report)
