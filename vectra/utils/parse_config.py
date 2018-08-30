# -*- coding: utf-8 -*-
"""
Created on Thu Sep 07 14:48:39 2017

@author: ldh
"""

# parse_config.py
import pandas as pd
from ..constants import TRANSACTION_FEE_DEFAULTS,TRANSACTION_FEE_ITEMS

class Config(object):
    
    def __init__(self,config):
        self.config = config
        self._parse_universe()
        self._generate_fee_table()
        
    def to_dict(self):
        return self.config
    
    @property
    def start_date(self):
        return self.config['base']['start_date']
    
    @property
    def end_date(self):
        return self.config['base']['end_date']
    
    @property
    def capital(self):
        return self.config['base']['capital']
    
    @property
    def frequency(self):
        return self.config['base']['frequency']
        
    @property
    def position_base(self):
        if 'position_base' in self.config['base'].keys():
            return self.config['base']['position_base']
        else:
            return None
        
    @property
    def cost_base(self):
        if 'cost_base' in self.config['base'].keys():
            return self.config['base']['cost_base']
        else:
            return None
        
    @property
    def source(self):
        return self.config['source']
    
    @property
    def file_path(self):
        return self.config['file_path']
    
    @property
    def benchmark_path(self):
        return self.config['benchmark_path']
    
    def _parse_universe(self):
        universe = self.config['base']['universe']
        if not isinstance(universe,list):
            print 'attribute universe must be a list'
            raise ValueError
        if len(universe) < 1:
            return []
        else:
            symbol = universe[0]
            if symbol in ['A','hs300','A-st','sz50']:
                pass
            else:
                self.universe = universe
                
    def _generate_fee_table(self):
        fee_table = pd.DataFrame([TRANSACTION_FEE_DEFAULTS] * len(self.universe),
                         index = self.universe,columns = TRANSACTION_FEE_ITEMS)
        self.fee_table = fee_table      
        if 'fee' not in self.config.keys():
            return 
        else:
            for key,val in self.config['fee'].items():
                self.fee_table.loc[key,:] = val
        
    
       
    
        

