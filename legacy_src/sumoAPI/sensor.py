#!/usr/bin/env python
"""
@file    sensor.py
@author  Simon Box
@date    31/01/2013

Classes for extracting sensor data from SUMO and simulating real world data 

"""
import traci

class sensor(object):
    pass

class censusSensor(sensor):
    
    def __init__(self,sensorID,aggregationPeriod=0):
        self.sensorID = sensorID
        self.aggregationPeriod = aggregationPeriod
        self.cumulativeCount = {}
        self.cumulativeOccupancy = {}
        self.occupiedLastStep = False
        
    def process(self):
        ##collect the latest data.
        occupied = traci.inductionloop.getLastStepOccupancy(self.sensorID)
        if occupied > 0:
            self.occupiedLastStep = True
            self.cumulativeOccupancy[traci.simulation.getCurrentTime()] = occupied
        elif occupied <= 0:
            self.cumulativeOccupancy[traci.simulation.getCurrentTime()] = 0
            if self.occupiedLastStep:
                self.cumulativeCount[traci.simulation.getCurrentTime()] = 1
            self.occupiedLastStep = False
        
        self.loopEliminateDictionary(self.cumulativeOccupancy)
        self.loopEliminateDictionary(self.cumulativeCount)
        
        
    def loopEliminateDictionary(self,dictionary):
        deleteList = []
        for time, value in dictionary.iteritems():
            if (traci.simulation.getCurrentTime() - time) > self.aggregationPeriod:
                deleteList.append(time)
        for deleteItem in deleteList:
            del dictionary[deleteItem] 
             
    def getAggregatedCount(self):
        addValues = self.sumOverDictionary(self.cumulativeCount)
        return addValues
    
    def getAggregatedOccupancy(self):
        addValues = self.sumOverDictionary(self.cumulativeOccupancy)
        return addValues/len(self.cumulativeOccupancy)
    
    def sumOverDictionary(self,dictionary):
        addValues = 0
        for time, value in dictionary.iteritems():
            addValues += value
        return addValues

class probeSensor(sensor):
    pass