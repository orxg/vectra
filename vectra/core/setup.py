# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:04:14 2017

@author: ldh
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
      ext_modules = cythonize('strategy.pyx'))

