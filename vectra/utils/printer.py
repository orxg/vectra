# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 13:12:13 2018

@author: ldh
"""

# printer.py

class ScreenPrinter():
    def __init__(self):
        self._active = False
        
    def turnon(self):
        self._active = True
        
    def shutdown(self):
        self._active = False

    def print_on_screen(self,text):
        if self._active:
            print text
    