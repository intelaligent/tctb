#!/usr/bin/env python
"""
@file    edgeObj.py
@author  Simon Box
@date    31/01/2013

Class for calculating all possible routes from a given node (with no U-turns). 
WARNING: don't use this for networks with circular routes or it will run for ever.

"""


class routesFromNode:
    
    def __init__(self,startingEdge,edgeStruct):
        self.edgeStruct = edgeStruct
        self.startingEdge=startingEdge
        self.completeRoutes=[]
        self.openRoutes=[]
        
        sRoute=[]
        sRoute.append(startingEdge)
        self.openRoutes.append(sRoute)
        
        while len(self.openRoutes) != 0:
            for route in self.openRoutes:
                self.openRoutes.remove(route)
                
                newRoutes = self.crawl(route)
                
                for nRoute in newRoutes:
                    self.openRoutes.append(nRoute)
            
        
    def crawl(self,route):
        protoRoutes=[]
        
        downstreamEdges = self.edgeStruct.getDownstreamEdges(route[-1])
        
        if len(downstreamEdges)==0:
            self.completeRoutes.append(route)
        else:
            for edge in downstreamEdges:
                pRoute = list(route)
                pRoute.append(self.edgeStruct.getEdgeName(edge))
                protoRoutes.append(pRoute)
                
        return(protoRoutes)