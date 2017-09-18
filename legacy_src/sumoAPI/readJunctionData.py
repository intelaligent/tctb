#!/usr/bin/env python
"""
@file    readJunctionData.py
@author  Simon Box
@date    31/01/2013

Class for reading a jcn.xml file and storing junctionObj and stageObj data.
//TODO join this class with 'readEdges' as common children of an abstract readXML class 
"""

from xml.dom.minidom import parse
import stageObj,junctionObj, unicodedata

class readJunctionData:
    
    def __init__(self,fileName):
        self.dom = parse(fileName)
    
    def getJunctionData(self):    
        junctionData = []
        
        for jcnNode in self.dom.getElementsByTagName('junction'):
            stageData=[]
            for stgNode in jcnNode.getElementsByTagName('stage'):
                id = unicodedata.normalize('NFKD',stgNode.getAttributeNode('id').nodeValue).encode('ascii','ignore')
                controlString = unicodedata.normalize('NFKD',stgNode.getAttributeNode('controlString').nodeValue).encode('ascii','ignore')
                period = float(unicodedata.normalize('NFKD',stgNode.getAttributeNode('period').nodeValue).encode('ascii','ignore'))
                stageData.append(stageObj.stageObj(id, controlString, period))
            
            juncID = unicodedata.normalize('NFKD',jcnNode.getAttributeNode('id').nodeValue).encode('ascii','ignore')
            offset = float(unicodedata.normalize('NFKD',jcnNode.getAttributeNode('offset').nodeValue).encode('ascii','ignore'))
            junctionData.append(junctionObj.junctionObj(juncID, stageData, offset))
            
        return junctionData
        