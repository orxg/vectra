# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 21:21:31 2017

@author: ldh
"""

# __init__.py

def id_gen(start=1):
    i = start
    while True:
        yield i
        i += 1
        
        
if __name__ == '__main__':
    id_g = id_gen()
    new_id = next(id_g)