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
import matplotlib as mpl
from matplotlib import gridspec
from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from color_names import color_names

from vectra.constants import ORDER_STATUS

def load_report(file_path):
    '''
    读取报告.
    '''
    with open(file_path,'r') as f:
        report = pickle.load(f)
    return report

def plot(report,save_path = None):
    '''
    根据报告做图.
    
    Parameters
    -------------
    report
        dict,vectra产生的报告
    save_path
        str,图片保存路径
    '''
    # 资产收益率曲线
    portfolio_return = pd.DataFrame(report['portfolio_value'],
                                    columns = ['calendar_dt',
                                               'trading_dt',
                                               'portfolio_value'])
    portfolio_return['portfolio_accumulate_return'] = \
    portfolio_return['portfolio_value'] / portfolio_return['portfolio_value'].values[0] - 1.0
    portfolio_return = portfolio_return[['calendar_dt','portfolio_accumulate_return']]
    
    # 统计指标
    statistic = describe(report)
    
    # 做图设定
    red = "#aa4643"
    black = "#000000"
    font_size = 14
    value_font_size = 13

    # 开始做图
    
    x_vals = portfolio_return['calendar_dt'].values
    y_vals = portfolio_return['portfolio_accumulate_return'].values
    N = len(x_vals)
    ind = np.arange(N)
    
    def format_date(x,pos=None):
        this_ind = np.clip(int(x+0.5),0,N-1)
        return pd.to_datetime(x_vals[this_ind]).strftime('%Y-%m-%d')
    
    plt.figure(figsize = (20,8))
    gs = gridspec.GridSpec(8,8)
    ax = plt.subplot(gs[:,:-1])
    ax.plot(ind,y_vals)
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_yticklabels(['{:.2%}'.format(y) for y in ax.get_yticks()])
    ax.grid(True)
    ax.set_title('Strategy Accumulate Return',fontsize = 25)
    ax.set_xlabel('Date',fontsize = 20)
    ax.set_ylabel('Accumulate Return',fontsize = 20)
   
    
    ax2 = plt.subplot(gs[:,-1])
    fig_data = [
            (0.01,0.9,0.85,'Total Returns','{0:.3%}'.format(statistic['total_return']),red,black),
            (0.01,0.8,0.75,'Annual Returns','{0:.3%}'.format(statistic['annual_return']),red,black),
            (0.01,0.7,0.65,'Max Drawdown','{0:.3%}'.format(statistic['max_drawdown']),red,black),
            (0.01,0.6,0.55,'Max Returns','{0:.3%}'.format(statistic['max_return']),red,black)]    
    
    for x,y1,y2, label, value, label_color, value_color in fig_data:
        ax2.text(x, y1, label, color=label_color, fontsize=font_size)
        ax2.text(x, y2, value, color=value_color, fontsize=value_font_size)
    ax2.xaxis.set_major_locator(ticker.NullLocator())
    ax2.yaxis.set_major_locator(ticker.NullLocator())
    
    if save_path is not None:
        plt.savefig(save_path)
      
def plot_with_benchmark(report,benchmark_path,save_path = None):
    '''
    根据报告做图.
    
    Parameters
    -------------
    report
        dict,vectra产生的报告
    benchmark_path
        str,基准数据路径
    save_path
        str,图片保存路径
    '''
    # 资产收益率曲线
    portfolio_return = pd.DataFrame(report['portfolio_value'],
                                    columns = ['calendar_dt',
                                               'trading_dt',
                                               'portfolio_value'])
    benchmark = pd.read_excel(benchmark_path,index_col = 0,parse_dates = True)
    portfolio_return = portfolio_return.join(benchmark,on = 'calendar_dt')
    portfolio_return.dropna(inplace = True)
    portfolio_return['portfolio_accumulate_return'] = \
    portfolio_return['portfolio_value'] / portfolio_return['portfolio_value'].values[0] - 1.0
    portfolio_return['benchmark_accumulate_return'] = \
    portfolio_return['close_price'] / portfolio_return['close_price'].values[0] - 1.0
    portfolio_return = portfolio_return[['calendar_dt','portfolio_accumulate_return','benchmark_accumulate_return']]
    portfolio_return['relative_accumulate_return'] = portfolio_return['portfolio_accumulate_return'] - \
    portfolio_return['benchmark_accumulate_return']
    
    # 统计指标
    statistic = describe(report)
    
    # 做图设定
    red = "#aa4643"
    black = "#000000"
    blue = '#0000FF'
    green = '#00FF7F'
    
    font_size = 14
    value_font_size = 13

    # 开始做图
    
    x_vals = portfolio_return['calendar_dt'].values
    y_vals1 = portfolio_return['portfolio_accumulate_return'].values
    y_vals2 = portfolio_return['benchmark_accumulate_return'].values
    y_vals3 = portfolio_return['relative_accumulate_return'].values
    
    N = len(x_vals)
    ind = np.arange(N)
    
    def format_date(x,pos=None):
        this_ind = np.clip(int(x+0.5),0,N-1)
        return pd.to_datetime(x_vals[this_ind]).strftime('%Y-%m-%d')
    
    plt.figure(figsize = (20,8))
    gs = gridspec.GridSpec(8,8)
    ax = plt.subplot(gs[:,:-1])
    ax.plot(ind,y_vals1,color = blue,label = 'Portfolio')
    ax.plot(ind,y_vals2,color = green,label = 'Benchmark')
    ax.plot(ind,y_vals3,color = red,label = 'Relative')
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_yticklabels(['{:.2%}'.format(y) for y in ax.get_yticks()])
    ax.grid(True)
    ax.set_title('Strategy Accumulate Return',fontsize = 25)
    ax.set_xlabel('Date',fontsize = 20)
    ax.set_ylabel('Accumulate Return',fontsize = 20)
    ax.legend(fontsize = 15)
    
    ax2 = plt.subplot(gs[:,-1])
    fig_data = [
            (0.01,0.9,0.85,'Total Returns','{0:.3%}'.format(statistic['total_return']),red,black),
            (0.01,0.8,0.75,'Annual Returns','{0:.3%}'.format(statistic['annual_return']),red,black),
            (0.01,0.7,0.65,'Max Drawdown','{0:.3%}'.format(statistic['max_drawdown']),red,black),
            (0.01,0.6,0.55,'Max Returns','{0:.3%}'.format(statistic['max_return']),red,black)]    
    
    for x,y1,y2, label, value, label_color, value_color in fig_data:
        ax2.text(x, y1, label, color=label_color, fontsize=font_size)
        ax2.text(x, y2, value, color=value_color, fontsize=value_font_size)
    ax2.xaxis.set_major_locator(ticker.NullLocator())
    ax2.yaxis.set_major_locator(ticker.NullLocator())
    
    
    if save_path is not None:
        plt.savefig(save_path)
        
def visualize_report(report,save_path = None):
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
    Tuple(order_detail,account_detail) DataFrame
    '''
    
    # 订单细节
    history_fill_orders = report['history_fill_orders']
    history_rejected_orders = report['history_rejected_orders']
    history_fill_orders = pd.DataFrame.from_dict(history_fill_orders)
    history_rejected_orders = pd.DataFrame.from_dict(history_rejected_orders)
    
    history_orders = pd.concat([history_fill_orders,history_rejected_orders])
    history_orders = history_orders.set_index('order_id')
    history_orders = history_orders.sort_index(ascending = True)
    history_orders = history_orders.reindex(columns = ['calendar_dt',
                                                       'trading_dt',
                                      'ticker','amount','direction',
                                      'order_price','order_state',
                                      'fill_dt','match_price','match_amount',
                                      'reject_reason','transaction_fee',
                                      'tax','commission_fee',
                                      'transfer_fee'])
    def transforme_order_state(row):
        if row == ORDER_STATUS.FILLED:
            return 'FILLED'
        elif row == ORDER_STATUS.REJECTED:
            return 'REJECTED'
        elif row == ORDER_STATUS.PARTIAL_FILLED:
            return 'PARTIAL_FILLED'
    history_orders['order_state'] = history_orders['order_state'].apply(\
                 transforme_order_state)
    
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
    
    # 现金记录
    cash_df = pd.DataFrame.from_records(report['daily_cash'],
                                       columns = ['calendar_dt',
                                                  'trading_dt',
                                                  'cash'])
    cash_df = cash_df[['calendar_dt','cash']].set_index('calendar_dt')  
    
    # 账户总资产
    portfolio_value_df = pd.DataFrame.from_records(report['daily_portfolio_value'],
                                       columns = ['calendar_dt',
                                                  'trading_dt',
                                                  'portfolio_value'])
    portfolio_value_df = portfolio_value_df[['calendar_dt','portfolio_value']].\
                    set_index('calendar_dt') 
    
    # 合并
    account_record = pd.concat([cash_df,portfolio_value_df],axis = 1)
    account_record['market_value'] = account_record['portfolio_value'] - \
                                    account_record['cash']   
    # 保存
    if save_path is not None:
        holding_record.to_excel(os.path.join(save_path,'holding_record.xlsx'))
        weight_record.to_excel(os.path.join(save_path,'weight_record.xlsx'))
        account_record.to_excel(os.path.join(save_path,'account_record.xlsx'))
        history_orders.to_excel(os.path.join(save_path,'history_orders.xlsx') )        
    # 返回
    return holding_record,weight_record,account_record,history_orders,

def describe(report):
    '''
    根据报告做统计描述.
    
    Parameters
    ----------
    report
        Dict,vectra report
        
    Returns
    ---------
    Series
        total_return
        annual_return
        max_drawdown
        max_return
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
    annual_ret = (1 + total_ret)**(365.0/duration_days) - 1.0
    
    # 最大回撤
    net_value = pd.DataFrame(report['daily_portfolio_value'],
                             columns = ['calendar_dt',
                                        'trade_dt',
                                        'value'])
    net_value.loc[:,'cum_max'] = net_value['value'].cummax()
    net_value.loc[:,'dd'] = (net_value['cum_max'] - net_value['value'])/ net_value['cum_max']
    max_dd = net_value['dd'].max()
    
    # 最高收益率
    max_net_value = net_value['value'].max()
    max_ret = (max_net_value - net_value['value'].iloc[0]) / net_value['value'].iloc[0]
        
    return pd.Series([total_ret,annual_ret,max_dd,max_ret],
                     index = ['total_return',
                              'annual_return',
                              'max_drawdown',
                              'max_return'])
    
def plot_history_weight(report,save_path = None):
    '''
    画历史仓位图。
    
    Parameters
    -------------
    report
        dict,vectra产生的报告
    save_path
        str,图片保存路径
    '''
    daily_weight = np.array(report['daily_weight'])[:,::2]
    
    weight_hist = pd.DataFrame.from_items(daily_weight)
    weight_hist = weight_hist.T
    weight_hist_cumsum = weight_hist.cumsum(axis = 1)
    weight_hist_sum = weight_hist.sum(axis = 1)
    
    fig,ax = plt.subplots(figsize = (20,10))
    ax.plot(weight_hist_cumsum.index,weight_hist_cumsum.values)
    ax.plot(weight_hist_sum.index,weight_hist_sum.values,color = 'k',
            label = 'TOTAL')    
    # Fill
    for idx in range(weight_hist_cumsum.shape[1]):
        if idx == 0:
            ax.fill_between(weight_hist_cumsum.index,
                        np.zeros(len(weight_hist_cumsum)),
                        weight_hist_cumsum.values[:,idx + 1],
                        color = color_names.values()[idx + 10],
                        label = weight_hist_cumsum.columns[idx])            
        else:
            ax.fill_between(weight_hist_cumsum.index,
                        weight_hist_cumsum.values[:,idx - 1],
                        weight_hist_cumsum.values[:,idx],
                        color = color_names.values()[idx + 10],
                        label = weight_hist_cumsum.columns[idx])
    # Others        
    ax.legend(fontsize = 16)
    ax.set_xlabel('Date',fontsize = 20)
    ax.set_ylabel('Holding Weight',fontsize = 20)
    ax.set_title('History Holding Weight',fontsize = 25)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend()
    
    if save_path is not None:
        fig.savefig(save_path)
        
if __name__ == '__main__':
    file_path = 'G:\\Work_ldh\\PM\\F1\\bt\\fof_f1_2.pkl'
    report = load_report(file_path)
    plot(report)
#==============================================================================
#     a = describe(report)
#     visualize_report(report,'G:\\Work_ldh\\PM\\F1\\bt2')
#==============================================================================
