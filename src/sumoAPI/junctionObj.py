#!/usr/bin/env python
"""
@file    junctionObj.py
@author  Simon Box
@date    31/01/2013

a container class for holding information about a junction for signal control
"""

class junctionObj:
    def __init__(self,id,stages,offset=None):
        self.id = id
        self.stages = stages
        self.offset = offset