#!/usr/bin/env python2
"""
@file    connection.py
@author  Bo Gao
@date    2017-07-25
@version alpha

Intersection Control Test Bed

Copyright (C) 2017 Transport Research Group, University of Southampton

Intersection Control Test Bed
"""
import os
import sys

import subprocess
import time


if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
    from sumolib import checkBinary # sumo, sumo-gui
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

class Connection:
    """ A SUMO TraCI connection """

    PORT_BASE = 45570

    def __init__(self, sumo_binary, network_path, sumo_net_file, sumo_additional_files, sumo_gui_settings_file, index):
        
        self.sumo_binary = sumo_binary

        self.network_path = network_path
        # self.sumo_config_file = sumo_config_file
        self.sumo_net_file = sumo_net_file
        self.sumo_additional_files = sumo_additional_files
        self.sumo_gui_settings_file = sumo_gui_settings_file

        self.index = index # 0,1,2,3...
        self.port = self.PORT_BASE + index

    def step(self):
        self.traci_connection.simulationStep()

    def open(self):
        command = []
        command.append(checkBinary(self.sumo_binary))
        command.append("--net-file")
        command.append(self.sumo_net_file)
        command.append("--additional-files")
        command.append(self.sumo_additional_files)
        command.append("--remote-port")
        command.append(str(self.port))
        command.append("--tripinfo-output")
        command.append(self.network_path + "/out_tripinfo.xml")
        command.append("--queue-output")
        command.append(self.network_path + "/out_queue.xml")
        command.append("--quit-on-end")
        command.append("--start")
        command.append("--step-method.ballistic")
        # command.append("--game")
        command.append("--summary-output")
        command.append(self.network_path + "/out_summary.xml")
        # command.append("--emission-output")
        # command.append(self.network_path + "/out_emission.xml")
        # command.append("--duration-log.statistics")
        # command.append("--full-output")
        # command.append(self.network_path + "/out_full.xml")
        # command.append("--osg-view")


        if self.sumo_binary == ConnectionManager.SUMO_BINARY_GUI :
            command.append("--gui-settings-file")
            command.append(self.sumo_gui_settings_file)

            command.append("--window-size")
            command.append("1000,700")
            command.append("--window-pos")
            if self.index < 2 :
                command.append(str(0 + self.index * 800) + ",0")
            else :
                command.append(str(0 + self.index * 200) + ",500")




        self.sp_popen = subprocess.Popen(command)

        time.sleep(.15)
        self.traci_connection = traci.connect(self.port)

        print("".join(elt+" " for elt in command))
        print(self.network_path + " connection established.")


    def close(self):
        self.traci_connection.close()
        print(self.network_path + " connection closed.")
        self.sp_popen.terminate()
        print(self.network_path + " sp terminated.")


class ConnectionManager:
    """ Manages a list of SUMO connections"""
    SUMO_BINARY_GUI = "sumo-gui"
    SUMO_BINARY_COMMAND_LINE = "sumo"

    sumo_binary = SUMO_BINARY_GUI #default

    def __init__(self):
        self.connection_list = []
        # print("Connection manager initialised\n")


    def reg_connection(self, network_path, sumo_net_file, sumo_additional_files, sumo_gui_settings_file):
        conn = Connection(self.sumo_binary,
                        network_path,
                        sumo_net_file,
                        sumo_additional_files,
                        sumo_gui_settings_file,
                        # self.PORT_BASE + 1 + len(self.connection_list),
                        len(self.connection_list)
            )
        self.connection_list.append(conn)
        return conn

    # def add_connection(self, sp_popen, traci_connection):
    #     self.connection_list.append(Connection(sp_popen, traci_connection))

    def step_all(self):
        for con in self.connection_list:
            con.step()

    def open_all(self):
        for con in self.connection_list:
            con.open()

    def close_all(self):
        for con in self.connection_list:
            con.close()