#!/usr/bin/env python
"""
@file    edgeObj.py
@author  Simon Box
@date    31/01/2013

Class for reading an edg.xml file and storing edgeObj data.

"""
from xml.dom.minidom import Document

class writeRoutes:
    
    def __init__(self,fileName):
        self.routesFile = open(fileName, "w")
        self.dom = Document();
        self.topNode = self.dom.createElement("routes")
        self.dom.appendChild(self.topNode)
        self.routeCount = 0
        
    def addRoutes(self,routeList):
        for route in routeList:
            thisRoute = self.dom.createElement("route")
            thisRoute.attributes["id"] = route[0] + 'TO' + route[-1]
            routeString=""
            for step in route:
                routeString += (step + " ")
            thisRoute.attributes["edges"] = routeString
            self.routeCount += 1
            self.topNode.appendChild(thisRoute)
            
    def printXML(self):
        print >> self.routesFile, self.dom.toprettyxml("    ")
    
    
        
        
            
        