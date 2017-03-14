#!/usr/bin/env python
"""
@file    signalControl.py
@author  Simon Box
@date    31/01/2013

Parent class for signal control algorithms

"""
import subprocess, sys, os, platform, time
from threading import Thread

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


class signalControl(object):
    
    def __init__(self, pathToConfig,gui):
        self.setPort(8813)
        programme = ""
        if gui:
            programme = "sumo-gui"
        else:
            programme = "sumo"
            
        self.sumoBinary = programme
        self.sumoConfig = pathToConfig
        if platform.system() == 'Windows':
            self.sumoBinary = checkBinary(programme)
            
        self.setAmberTime(3)
        self.setAllRedTime(1)
        self.TRACI = traci
        self.isConnected = False
        
    
    def launchSumoAndConnect(self):
        try:
            sumoProcess = subprocess.Popen("%s -c %s" % (self.sumoBinary, self.sumoConfig), shell=True, stdout=sys.stdout)
            traci.init(self.Port)
            self.isConnected = True
        except Exception:
            print "failed to connect to SUMO over the API: %s" % (Exception.message)
            
    def disconnect(self):
        self.isConnected = False
        traci.close()
        sys.stdout.flush()
      
    def setAmberTime(self,time):
        self.amberTime = time
        
    def setAllRedTime(self,time):
        self.allRed = time
        
    def setPort(self,port):
        self.Port = port
        
    def getCurrentSUMOtime(self):
        return traci.simulation.getCurrentTime()
        
    class stageTransition(Thread):     
        def run(self,junctionID,currentStageString,targetStageString,amberTime = None,allRed = None):
            success = True
            if amberTime==None:
                amberTime = self.amberTime
            if allRed==None:
                allRed = self.allRed
                
            if len(currentStageString) != len(targetStageString):
                print "Error current stage string and target stage sting are different lengths"
                success=False
            
            amberStageString=""
            allRedStageString=""
            i=0
            while i < len(currentStageString):
                if targetStageString[i]=='r' and (currentStageString[i]=='G' or currentStageString[i]=='g'):
                    amberStageString = amberStageString + 'y'
                    allRedStageString = allRedStageString + 'r'
                else:
                    amberStageString = amberStageString + currentStageString[i]
                
                i+=1
                
            try:
                traci.trafficlights.setRedYellowGreenState(junctionID, amberStageString)
                transitionStart = self.getCurrentSUMOtime()
                while (self.getCurrentSUMOtime() - transitionStart) < (amberTime*1000):
                    pass
                    
                traci.trafficlights.setRedYellowGreenState(junctionID, allRedStageString)
                while (self.getCurrentSUMOtime() - transitionStart) < ((amberTime+allRed)*1000):
                    pass
                    
                traci.trafficlights.setRedYellowGreenState(junctionID, targetStageString)
            except Exception:
                print "failed to set the lights correctly: %s" % (Exception.message)
                success=False
                
            return success 