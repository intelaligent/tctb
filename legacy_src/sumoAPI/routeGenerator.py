#!/usr/bin/env python
"""
@file    routeGenerator.py
@author  Simon Box
@date    31/01/2013

Code to generate a routes file for the "simpleT" SUMO model.

"""

import random 
import readEdges
import routesFromNode
import writeRoutes
import sys

if len(sys.argv) > 1:
	edgeFile = sys.argv[0]
	routeFile = sys.argv[1]
elif len(sys.argv) == 1:
	edgeFile = sys.argv[0]
	routeFile = "output.rou.xml"
else:
	print "Error please supply "#TODO make this less crap

edgeData =readEdges.readEdges("corridor.edg.xml")

startingEdges=["6:4","9:8","11:10","13:12","15:14","17:16","19:18","7:5"]
routeFile = writeRoutes.writeRoutes("corridor.rou.xml")

for edge in startingEdges:
	rFN = routesFromNode.routesFromNode(edge,edgeData)
	routeFile.addRoutes(rFN.completeRoutes)

routeFile.printXML()




