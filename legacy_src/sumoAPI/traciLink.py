#!/usr/bin/env python
"""
@file    traciLink.py
@author  Simon Box
@date    31/01/2013

code snippet for determining the operating system and embedding the traci library link as a class member

"""
import sys, os, platform


#Test to see if we're running on linux or windows
if platform.system() == 'Linux':
    sys.path.append('/usr/share/sumo/tools')
elif platform.system() == 'Windows':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'tools'))
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), '..', '..', '..')), 'tools'))

try:
    from sumolib import checkBinary
    import traci
except Exception:
    print "failed to import traci or sumolib library, please make sure these libraries are on your Python path."

