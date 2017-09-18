#!/usr/bin/env python2
"""
@file    connection.py
@author  Bo Gao
@date    2017-07-25
@version alpha

Intersection control agent

Copyright (C) 2017 Transport Research Group, University of Southampton

Intersection Control Test Bed
"""
# if "SUMO_HOME" in os.environ:
#     tools = os.path.join(os.environ["SUMO_HOME"], "tools")
#     sys.path.append(tools)
#     from sumolib import checkBinary # sumo, sumo-gui
# else:   
#     sys.exit("please declare environment variable 'SUMO_HOME'")

# import traci

import os
import sys

from subprocess import call

class Agent:
    _name = ""

    def __init__(self, name):
        self._name = name

class Agent_Tools:
    """
    doc: http://www.sumo.dlr.de/userdoc/DUAROUTER.html
    duarouter
        -n data/map.sumo.net.xml
        -t demands/odTrips.demand.xml
        -d add.vTypes.xml
        -o demands/odTrips.rou.xml
    """


    def trip_to_route(self, scn):

        _binary_name = "duarouter"

        if "SUMO_HOME" in os.environ:
            tools = os.path.join(os.environ["SUMO_HOME"], "tools")
            sys.path.append(tools)
            from sumolib import checkBinary # sumo, sumo-gui
        else:   
            sys.exit("please declare environment variable 'SUMO_HOME'")

        output_route_file = os.path.join(scn.get("dir"), "duarouter_out.rou.xml")

        command = []
        command.append(checkBinary(_binary_name))
        command.append("--net-file")
        command.append(scn.get("net_file"))
        # command.append("--trip-files")
        # command.append(scn.get("demand_file"))
        command.append("--additional-files")
        command.append(scn.get("add_files"))
        command.append("--output-file")
        command.append(output_route_file)

        print("".join(elt + " " for elt in command))

        call(command)

        return output_route_file

class Agent_Sumo_Coordinator:
    """
    doc: http://www.sumo.dlr.de/userdoc/Tools/tls.html#tlsCoordinator.py
    tlsCoordinator.py 
        -n data/map.sumo.net.xml 
        -r demands/randomTrips.rou.xml 
        -o tls/tls.coordinated.xml
    """

    _script_name = "tlsCoordinator.py"

    def init(self, scn) :

        command = []

        tls_offset_file = os.path.join(scn.get("dir"), "tls.offset.sumo_coordinator.xml" )

        if "SUMO_HOME" in os.environ:
            command.append(os.path.join(os.environ["SUMO_HOME"], "tools", self._script_name))
        else:   
            sys.exit("Agent_Sumo_Coordinator requires environment variable 'SUMO_HOME'")

        command.append("--net-file")
        command.append(scn.get("net_file"))
        command.append("--route-file")
        command.append(Agent_Tools().trip_to_route(scn))
        command.append("--output-file")
        command.append(tls_offset_file)

        print("".join(elt + " " for elt in command))

        call(command)

        scn.add_additional_file(tls_offset_file)

class Agent_Sumo_Cycle_Adaptation:
    """
    doc: http://www.sumo.dlr.de/userdoc/Tools/tls.html#tlsCycleAdaptation.py
    tlsCycleAdaptation.py
        -n data/map.sumo.net.xml
        -r demands/odTrips.rou.xml
        -o tls/tls.ca.od.xml
    """

    _script_name = "tlsCycleAdaptation.py"
    
    def init(self, scn) :
        command = []

        tls_new_program_file = os.path.join(scn.get("dir"), "tls.offset.sumo_cycle_adaptation.xml" )

        if "SUMO_HOME" in os.environ:
            command.append(os.path.join(os.environ["SUMO_HOME"], "tools", self._script_name))
        else:   
            sys.exit("Agent_Sumo_Coordinator requires environment variable 'SUMO_HOME'")

        command.append("--net-file")
        command.append(scn.get("net_file"))
        command.append("--route-file")
        command.append(Agent_Tools().trip_to_route(scn))
        command.append("--output-file")
        command.append(tls_new_program_file)

        print("".join(elt + " " for elt in command))

        call(command)

        scn.add_additional_file(tls_new_program_file)

class AgentManager:

    def initialise_agent_for_scenario(self, scn):
        return {
            "tls_sumo_coordinator" : lambda scn : Agent_Sumo_Coordinator().init(scn),
            "tls_sumo_cycle_adaptation" : lambda scn : Agent_Sumo_Cycle_Adaptation().init(scn)
        }[scn.get("agent_type")](scn)
