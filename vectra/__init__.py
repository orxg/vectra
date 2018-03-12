# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 14:00:35 2017

@author: ldh
"""

# __init__.py
import logging
import yaml
import os

from .constants import BACKTEST,PAPER_TRADING,EASY_MODE,HARD_MODE

package_path = __path__[0]
etc_path = os.path.join(package_path,'etc.yaml')

with open(etc_path,'r') as f:
    etc = yaml.load(f)

def run_file(config,strategy_name,strategy_path,data_mode = 'e',mode = 'b',
             persist_path = None,report_path = None,if_test = False,
             log_path = None,verbose = False):
    '''
    Parameters
    ----------
    config
        用户策略配置
    strategy_name
        策略名称
    strategy_path
        策略路径
    mode
        模式 'b','p','r',支持回测'b'和模拟'p'
    data_mode
        数据模式,'e'前复权,'h'不复权
    persist_path
        在模拟状态下必须给出持久化路径
    report_path
        回测结果保存地址
    if_test
        bool,是否是系统测试
    log_path
        系统日志路径
    verbose
        bool,是否输出其他信息
    '''
    if log_path is not None:
        logging.basicConfig(filename = log_path,level = logging.DEBUG)
        
    if data_mode == 'e':
        data_mode = EASY_MODE
    elif data_mode == 'h':
        data_mode = HARD_MODE
        
    if mode == 'p':
        mode = PAPER_TRADING
    elif mode == 'b':
        mode = BACKTEST

        
    if report_path is None:
        report_path = etc['report_path']
    if mode == PAPER_TRADING and persist_path is None:
        persist_path = etc['persist_path']
                
    from .main import all_system_go
    return all_system_go(config,strategy_name,strategy_path,data_mode,mode,
                         persist_path,report_path,if_test=if_test,
                         verbose = verbose)
    
def run_weight(config,strategy_name,weight_path,data_mode = 'e',mode = 'b',
             persist_path = None,report_path = None,if_test = False,
             log_path = None,verbose = False):
    '''
    Run the strategy based on the weight data.
    
    Parameters
    ----------
    config
        用户策略配置
    strategy_name
        策略名称
    weight_path
        权重数据所在地址
    mode
        模式 'b','p','r',支持回测'b'和模拟'p'
    data_mode
        数据模式,'e'前复权,'h'不复权
    persist_path
        在模拟状态下必须给出持久化路径
    report_path
        回测结果保存地址
    if_test
        bool,是否是系统测试
    log_path
        系统日志路径
    verbose
        bool,是否输出其他信息
    '''
    if log_path is not None:
        logging.basicConfig(filename = log_path,level = logging.DEBUG)
        
    if data_mode == 'e':
        data_mode = EASY_MODE
    elif data_mode == 'h':
        data_mode = HARD_MODE
        
    if mode == 'p':
        mode = PAPER_TRADING
    elif mode == 'b':
        mode = BACKTEST
        
        
    if report_path is None:
        report_path = etc['report_path']
    if mode == PAPER_TRADING and persist_path is None:
        persist_path = etc['persist_path']
                
    strategy_path = package_path + '\\def\\bt_by_w.py'
    
    from .main import all_system_go
    return all_system_go(config,strategy_name,strategy_path,data_mode,mode,
                         persist_path,report_path,if_test=if_test,
                         weight_path = weight_path,verbose = verbose)