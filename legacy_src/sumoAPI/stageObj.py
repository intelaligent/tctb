#!/usr/bin/env python
"""
@file    stageObj.py
@author  Simon Box
@date    31/01/2013

a container class for holding information about a stage of a junction for signal control
"""

class stageObj:
    def __init__(self,id,controlString,period=None):
        self.id = id
        self.controlString = controlString
        self.period = period