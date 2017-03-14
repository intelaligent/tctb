#!/usr/bin/env python
"""
@file    trafcodLink.py
@author  Simon Box and Peter Knoppers
@date    13/02/2013

class for managing connection to trafcod

"""

import socket, re, sys, subprocess

class trafcodLink(object):
    def __init__(self,host,port):
        serverAddress=(host,port)
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(serverAddress)
        self.sock.settimeout(30)#Throws a timeout exception if connections are idle for 10 seconds
        self.sock.listen(1)#set the socket to listen, now it's a server!
        self.connected = False
        
    def handshakeTrafcod(self):
        try:
            while True:
                # Wait for a connection
                self.connection, self.clientAddress = self.sock.accept() 
                if self.connection != None:
                    self.connected = True
                    break
        except Exception:
            print "Failed handshake with Trafcod: %s" % (Exception.message)
            
    def launchTrafcod(self,trafcodExe, configFile):
        try:
            sumoProcess = subprocess.Popen("%s %s trafcod://%s:%s" % (trafcodExe, configFile, self.sock.getsockname()[0], self.sock.getsockname()[1]), shell=True, stdout=sys.stdout)
        except Exception:
            print "Failed to launch Trafcod: %s" % (Exception.message)
            
    def sendDetectorToTrafcod(self,detectorID,state):
        stateString = ""
        if state == 1:
            stateString = "occupied"
        elif state == 0:
            stateString = "empty"
        else:
            print "Cannot interpret state"
            
        message = "detector <%s> <%s>\r\n" % (detectorID,stateString)
        try:
            self.connection.sendall(message)
        except Exception:
            print "Failed to send detector data to TrafCod: %s" % (Exception.message)
        
    def askTrafcodToAdvance(self):
        message = "step\r\n"
        try:
            self.connection.sendall(message)
        except Exception:
            print "failed to advance TrafCod: %s" % (Exception.message)
        
    def recieveTrafcodLightStates(self):##//TODO make sure this function copes with \r\n and does not break until ready is received....
        dataString =""
        try:
            while True:
                incomingData = self.connection.recv(64)
                if incomingData:
                    if "ready" in incomingData:
                        break
                    else:
                        dataString += incomingData
                else:
                    break
        except Exception:
            print "failed to receive light data from TrafCod: %s" % (Exception.message)
            
        
        splitToJunctions = dataString.split('\r\n')
        junctionData = []
        for lightDataString in splitToJunctions:
            if "light" in lightDataString:
                splitData = re.split('<|>', lightDataString)
                junctionID = splitData[1]
                controlString = splitData[3]
                junctionData.append((junctionID,controlString))
        
        return junctionData
    
    def closeTrafcod(self):
        self.connection.close()
        self.sock.close()
        sys.stdout.flush()
    
    
        