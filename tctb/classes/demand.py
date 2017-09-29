#!/usr/bin/env python2
"""
@file    demand.py
@author  Bo Gao
@date    2017-08-14
@version alpha

Demand related

Copyright (C) 2017 Transport Research Group, University of Southampton

Intersection Control Test Bed
"""

import os
import sys

from subprocess import call

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
    import randomTrips
    from sumolib import checkBinary # od2trips
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Demand(object):
    """Demand Interface"""

    def generate(self):
        raise NotImplementedError( "Method generate not implemented." )

class Demand_RandomTrips(Demand):
    """randomTrips.py usage: http://sumo.dlr.de/wiki/Tools/Trip#randomTrips.py"""

    def generate(self, scn):
        randomTrips.main(
            randomTrips.get_options([
                "-n", scn.get("net_file"),
                # "-o", scenario_dir + "/data/model.trip.xml",
                "-o", scn.get("demand_file"),
                "--route-file", os.path.join(
                                    scn.get("dir"),
                                    scn.get("demand_type") + ".rou.xml"
                                ),
                "--prefix", scn.get("prefix"),
                "--fringe-factor", "100",
                "--validate"
            ])
        )
        print("DM/RT/generate")

class Demand_ODTrips(Demand):
    """od2trips usage: http://sumo.dlr.de/wiki/OD2TRIPS"""

    _od_binary = "od2trips"

    def generate(self, scn):

        command = []
        command.append(checkBinary(self._od_binary))
        command.append("--output-file")
        command.append(scn.get("demand_file"))
        command.append("--prefix")
        command.append(scn.get("prefix"))

        # command.append("--vtype")
        # command.append(scn.get("vType"))

        command.append("--taz-files")
        command.append(scn.get("taz_file"))

        if not scn.get("amitran_file") == "" :

            command.append("--od-amitran-files")
            command.append(scn.get("amitran_file"))

        elif not scn.get("matrix_file") == "" :

            command.append("--od-matrix-files")
            command.append(scn.get("matrix_file"))

        else :

            sys.exit("Error generating trips from OD using command: \n"
                        + "".join(elt+" " for elt in command))


        call(command)

        print("".join(elt+" " for elt in command))
        print("DM/OD/generated")

class DemandManager:

    # def __init__(self):
    #     self.type_rt = Demand_RandomTrips()
    #     self.type_odt = Demand_ODTrips()

    def get_demand(self, scn):
        return {
            # "randomTrips" : Demand_RandomTrips().generate(scn),
            # "odTrips" : Demand_ODTrips().generate(scn)
            "randomTrips" : lambda scn : Demand_RandomTrips().generate(scn),
            "odTrips" : lambda scn : Demand_ODTrips().generate(scn)
        # }.get(scn.get("demand_type"), self.type_rt.generate(scn))
        }[scn.get("demand_type")](scn)

        