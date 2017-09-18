#!/usr/bin/env python
"""
@file    fixedTimeControl.py
@author  Simon Box
@date    31/01/2013

class for fixed time signal control

"""
import signalControl, readJunctionData, traci

class keyControl(signalControl.signalControl):
    def __init__(self, junctionData):
        super(keyControl, self).__init__()
        self.junctionData = junctionData
        self.firstCalled = self.getCurrentSUMOtime()
        self.lastCalled = self.getCurrentSUMOtime()
        self.lastStageIndex = 0
        traci.trafficlights.setRedYellowGreenState(self.junctionData.id, 
            self.junctionData.stages[self.lastStageIndex].controlString)
        self.keyMap = {'Key.up':0, 'Key.right':3, 'Key.down':2, 'Key.left':1}

    def process(self, keyValue):
        # If the transition object is active i.e. processing a transition pass
        if self.transitionObject.active:
            pass
        # Else the light is not transitioning so we can change if needed
        else:
            # If the last key press is different than the current stage then
            # transition to that stage else do nothing
            if keyValue in self.keyMap.keys():
                desiredStageindex = self.keyMap[keyValue]
                if desiredStageindex != self.lastStageIndex:
                    # transition junctionID from laststage to nextStage
                    self.transitionObject.newTransition(
                        self.junctionData.id, 
                        self.junctionData.stages[self.lastStageIndex].controlString,
                        self.junctionData.stages[desiredStageindex].controlString)
                    self.lastStageIndex = desiredStageindex

                self.lastCalled = self.getCurrentSUMOtime()
                
        super(keyControl, self).process()
