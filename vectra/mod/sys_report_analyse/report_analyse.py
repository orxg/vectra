# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:30:39 2017

@author: ldh
"""

# report_analyse.py

import numpy as np
import pandas as pd
from vectra.utils.analyse.analyse import plot,plot_history_weight,plot_with_benchmark
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

class ReportAnalyser():
    def __init__(self):
        pass
    
    def plot(self,report):
        '''
        根据报告做图.
        '''
        plot(report)
        
    def plot_history_weight(self,report):
        plot_history_weight(report)
        
    def plot_with_benchmark(self,report,benchmark_path):
        plot_with_benchmark(report,benchmark_path)
