# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 20:40:35 2017

@author: ldh
"""

# main.py
import datetime

from .constants import BACKTEST,PAPER_TRADING
from .events import EVENT,Event
from .environment import Environment
from .core.engine import Engine
from .core.strategy import Strategy
from .core.strategy_loader import StrategyLoader
from .core.dynamic_universe import DynamicUniverse
from .core.context import Context
from .data.data_proxy import DataProxy
from .data.data_source.podaci_data_source.podaci_data_source import PodaciDataSource
from .model.analyser import Analyser
from .model.bar import BarMap
from .mod import ModHandler
from .utils.parse_config import Config
from .utils.create_base_scope import create_base_scope
from .utils.persist_provider import DiskPersistProvider
from .utils.persist_helper import PersistHelper
from .api.helper import get_apis

def all_system_go(config,strategy_name,strategy_path,data_mode,mode,
                  persist_path = None,report_path = None):
    '''
    主程序。启动回测/模拟/实盘。
    
    Parameters
    ----------
        config
            策略配置
        strategy_name
            策略名称
        strategy_path
            策略路径
        data_mode
            数据模式
        mode
            运行模式
        persist_path
            持久化路径,模拟专有
        report_path
            报告保存地址
    '''
    config = Config(config)
    env = Environment(config)
            
    if mode == BACKTEST:
        MOD_LIST = ['sys_simulation']

    elif mode == PAPER_TRADING:
        MOD_LIST = ['sys_email_sender','sys_paper_trading']                
    
    #%% 数据模式与运行模式
    env.data_mode = data_mode
    env.mode = mode    
    
    #%% 策略读取
    scope = create_base_scope()
    strategy_loader = StrategyLoader(strategy_path)
    apis = get_apis()
    scope.update(apis)
    scope = strategy_loader.load(scope)
    print 'Loading strategy scope successfully'
    
    #%% 数据源与代理载入环境
    env.set_data_source(PodaciDataSource())  
    env.set_data_proxy(DataProxy(env.data_source,data_mode=data_mode,mode=mode))
    print 'Loading data source & data_proxy successfully'
    
    #%% MOD载入环境(事件源,撮合,账户)
    mod_handler = ModHandler(MOD_LIST)
    mod_handler.set_env(env)
    mod_handler.start_up()
    print 'Loading mods successfully'
    
    #%% 动态股票池载入环境
    dynamic_universe = DynamicUniverse()
    env.set_dynamic_universe(dynamic_universe)
    print 'Loading dynamic universe successfully'
    
    #%% 记录/分析工具载入环境
    if report_path is None:
        pass
    env.set_analyser(Analyser(env,strategy_name,report_path))
    print 'Loading analyser successfully'
    
    #%% Strategy对象载入环境
    user_context = Context()
    env.set_context(user_context)
    bar_map = BarMap(env)
    env.set_bar_map(bar_map)
    strategy = Strategy(env,scope,user_context,bar_map)
    assert strategy is not None
    strategy.initilize()
    print 'Loading strategy successfully'
    
    #%% 持久化注册(模拟专有)
    if mode == PAPER_TRADING:
        persist_provider = DiskPersistProvider(persist_path)
        persist_helper = PersistHelper(persist_provider,env.event_bus,mode)
        persist_helper.rigister('user_context',user_context)
        persist_helper.rigister('account',env.account)
        persist_helper.rigister('analyser',env.analyser)
    
        ### 从硬盘中恢复到最新的状态
        persist_helper.restore()
        print 'Restore previous strategy status successfully'
        
    #%% 启动引擎
    print 'The system engine is going to run right now...'
    env.event_bus.publish_event(Event(EVENT.SYSTEM_INITILIZE))
    Engine(env).run()

    #%% 获取报告
    report = env.analyser.report()
    
    print 'Get the report successfully'
    #%% 收尾
    mod_handler.tear_down()
    
    return report
        
        
    
    