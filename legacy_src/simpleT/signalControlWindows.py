#!/usr/bin/env python
"""
@file    signalControl.py
@author  Simon Box
@date    31/01/2013

Code to control the traffic lights in the "simpleT" SUMO model.

"""

import os, subprocess, sys, random
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'tools'))
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), '..', '..', '..')), 'tools'))
from sumolib import checkBinary
import traci

PORT = 8813

stage01="GGgrrrrGGG"
inter0102="GGgrrrryyy"
stage02="GGGrrrrrrr"
inter0203="yyyrrrrrrr"
stage03="rrrGGGGrrr"
inter0301="rrryyyyrrr"

Stages=[stage01,stage03];

sumoBinary = checkBinary('sumo')
    sumoConfig = "data/cross.sumocfg"
    if len(sys.argv) > 1:
        retCode = subprocess.call("%s -c %s --python-script %s" % (sumoBinary, sumoConfig, __file__), shell=True, stdout=sys.stdout)
        sys.exit(retCode)
    else:
        sumoProcess = subprocess.Popen("%s -c %s" % (sumoBinary, sumoConfig), shell=True, stdout=sys.stdout)

traci.init(PORT)

step = 0
lastSwitch=0;
stageIndex = 0;
while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    timeNow = traci.simulation.getCurrentTime()
    lO1Count = traci.inductionloop.getLastStepVehicleNumber("0") + traci.inductionloop.getLastStepVehicleNumber("1") 
    l23Count = traci.inductionloop.getLastStepVehicleNumber("2") + traci.inductionloop.getLastStepVehicleNumber("3") 	    
    if timeNow-lastSwitch > 10000:
        if stageIndex==0:
            stageIndex=1;
        else:
            stageIndex=0;
        traci.trafficlights.setRedYellowGreenState("1", Stages[stageIndex])
        
    
    step += 1

traci.close()
sys.stdout.flush()
