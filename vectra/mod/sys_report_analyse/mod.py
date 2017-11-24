# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:25:55 2017

@author: ldh
"""

# mod.py

from vectra.interface import AbstractMod
from report_analyse import ReportAnalyser

class ReportAnalyseMod(AbstractMod):
    def __init__(self):
        pass
    
    def start_up(self,env):
        '''
        启动该mod.
        '''
        env.report_analyser = ReportAnalyser()
    
    def tear_down(self):
        '''
        关闭mod.
        '''
        pass
    
