#!/usr/bin/env python
"""
@file    signalControl.py
@author  Simon Box
@date    31/01/2013

Parent class for signal control algorithms

"""
import traciLink, traci


class signalControl(object):
    
    def __init__(self):
        self.transitionObject = stageTransition()
        
    def process(self):
        self.transitionObject.processTransition()
        
    def getCurrentSUMOtime(self):
        return traci.simulation.getCurrentTime()
    
    def setAmberTime(self, time):
            self.transitionObject.setAmberTime(time)
        
    def setAllRedTime(self, time):
            self.transitionObject.setAllRedTime(time)
    
    
class stageTransition(object):
        
        def __init__(self): 
            self.setAmberTime(3)
            self.setAllRedTime(1)
            self.active=False
        
        def setAmberTime(self, time):
            self.amberTime = time
        
        def setAllRedTime(self, time):
            self.allRed = time
            
        def getCurrentSUMOtime(self):
            return traci.simulation.getCurrentTime()
            
        def newTransition(self, junctionID, currentStageString, targetStageString):
            if len(currentStageString) != len(targetStageString):
                print "Error current stage string and target stage sting are different lengths"
            
            self.amberStageString=""
            self.allRedStageString=""
            i = 0
            while i < len(currentStageString):
                if targetStageString[i]=='r' and (currentStageString[i]=='G' or currentStageString[i]=='g'):
                    self.amberStageString = self.amberStageString + 'y'
                    self.allRedStageString = self.allRedStageString + 'r'
                else:
                    self.amberStageString = self.amberStageString + currentStageString[i]
                    self.allRedStageString = self.allRedStageString + currentStageString[i]
                i += 1
            
            self.targetStageString = targetStageString
            self.junctionID = junctionID
            self.transitionStart = self.getCurrentSUMOtime()
            self.active = True
            
        def processTransition(self):             
            if self.active:
                if (self.getCurrentSUMOtime() - self.transitionStart) < (self.amberTime*1000):
                    traci.trafficlights.setRedYellowGreenState(self.junctionID, self.amberStageString)
                elif (self.getCurrentSUMOtime()- self.transitionStart) < ((self.amberTime + self.allRed)*1000):
                    traci.trafficlights.setRedYellowGreenState(self.junctionID, self.allRedStageString)
                else:
                    traci.trafficlights.setRedYellowGreenState(self.junctionID, self.targetStageString)
                    self.active=False
            else:
                pass
                 