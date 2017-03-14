#!/usr/bin/env python
"""
@file    readEdges.py
@author  Simon Box
@date    31/01/2013

Class for reading an edg.xml file and storing edgeObj data.

"""
from xml.dom.minidom import parse

class readEdges:
    
    def __init__(self,filePath):
        self.dom = parse(filePath)
        #for node in dom.getElementsByTagName('edge'):    
    
    
    def getEdgeElementByName(self,name):
        
        for node in self.dom.getElementsByTagName('edge'):
            if name == node.getAttributeNode('id').nodeValue:
                returnNode = node
        
                
        return(returnNode)
    
    def getDownstreamEdges(self,edgeName):
        listOfEdges=[]
        
        interestEdge = self.getEdgeElementByName(edgeName)
        
        frm = interestEdge.getAttributeNode('from').nodeValue
        to = interestEdge.getAttributeNode('to').nodeValue
        
        for node in self.dom.getElementsByTagName('edge'):
            if (to==node.getAttributeNode('from').nodeValue and frm!=node.getAttributeNode('to').nodeValue):
                listOfEdges.append(node)
                
        return(listOfEdges)
    
    def getEdgeName(self,edge):
        return(edge.getAttributeNode('id').nodeValue)
    
    