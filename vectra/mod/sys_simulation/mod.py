# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:25:19 2017

@author: ldh
"""

# mod.py

from .simulation_broker import SimulationBroker
from .simulation_event_source import SimulationEventSource
from .simulation_account import SimulationAccount
from vectra.interface import AbstractMod

class SimulationMod(AbstractMod):
    def __init__(self):
        pass
    
    def start_up(self,env):
        '''
        启动该mod.
        '''
        env.set_broker(SimulationBroker(env))
        env.set_event_source(SimulationEventSource(env))
        env.set_account(SimulationAccount(env))
        
    def tear_down(self):
        pass
    
    

