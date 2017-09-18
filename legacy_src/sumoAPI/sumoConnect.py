#!/usr/bin/env python
"""
@file    sumoConnect.py
@author  Simon Box
@date    31/01/2013

Parent class for signal control algorithms

"""
import traciLink, platform, subprocess, sys, traci

class sumoConnect(object):
    
    def __init__(self, pathToConfig, gui, port=8813):
        self.setPort(port)
        programme = ""
        if gui:
            programme = "sumo-gui"
        else:
            programme = "sumo"
            
        self.sumoBinary = programme
        self.sumoConfig = pathToConfig
        if platform.system() == 'Windows':
            self.sumoBinary = self.checkBinary(programme)
            
        self.isConnected = False
        
    
    def launchSumoAndConnect(self):
        try:
            sumoProcess = subprocess.Popen("%s -c %s" % (self.sumoBinary, self.sumoConfig), shell=True, stdout=sys.stdout)
            traci.init(self.Port)
            self.isConnected = True
        except Exception:
            print "failed to connect to SUMO over the API: %s" % (Exception.message)
            
    def runSimulationForSeconds(self, seconds):
        start = self.getCurrentSUMOtime()
        while (self.getCurrentSUMOtime() - start) < (seconds*1000):
            traci.simulationStep()
    
    def runSimulationForOneStep(self):
            traci.simulationStep()
            
    def getCurrentSUMOtime(self):
        return traci.simulation.getCurrentTime()
    
    
    def disconnect(self):
        self.isConnected = False
        traci.close()
        sys.stdout.flush()
    
        
    def setPort(self, port):
        self.Port = port