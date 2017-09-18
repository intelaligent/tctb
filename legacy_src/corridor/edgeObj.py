#!/usr/bin/env python
"""
@file    edgeObj.py
@author  Simon Box
@date    31/01/2013

Class for holding edge data.

"""

class edgeObj(object):
    
    def __init__(self,name,frm,to):
        self.name = name
        self.frm = frm
        self.to = to