#!/usr/bin/env python2
"""
@file    scenario.py
@author  Bo Gao
@date    2017-08-14
@version alpha

Scenario

Copyright (C) 2017 Transport Research Group, University of Southampton

Intersection Control Test Bed
"""

import os
# import sys

import static_xml as static_xml

from demand import DemandManager
from connection import ConnectionManager
from agent import AgentManager

class Scenario:
    """ A Scenario """

    def __init__(self, work_dir, scenario_config, index):

        self.work_dir = work_dir
        self.index = index # 0,1,2...
        self.prefix = "scenario_" + str(self.index) + "_"

        if scenario_config.get("name") :
            self.name = scenario_config.get("name")
        else :
            self.name = str(self.index)

        self.scenario_network_config = scenario_config.find("network")
        self.net_file = ""
        self.additional_files = ""
        self.gui_settings_files = ""

        self.scenario_demand_config = scenario_config.find("demand")
        self.demand_type = ""
        self.taz_file = ""
        # self.od_format = ""
        self.amitran_file = ""
        self.matrix_file = ""
        self.vType = "tctb_default"

        self.scenario_agent_config = scenario_config.find("agent")
        self.agent_type = ""

        self.connection = None


        # 1/3 Read Network Configurations
        if not self.scenario_network_config.get("sumo_net_file"):
            self.net_file = os.path.join(
                                self.work_dir,
                                "data",
                                "model.net.xml"
                            ) 
        else :
            self.net_file = os.path.join(
                                self.work_dir,
                                self.scenario_network_config.get("sumo_net_file")
                            )

        if not self.scenario_network_config.get("sumo_additional_files"):
            self.additional_files = "" 
        else :
            self.additional_files = "".join(os.path.join(self.work_dir, elt)+"," for elt in self.scenario_network_config.get("sumo_additional_files").split(","))[:-1]

        if not self.scenario_network_config.get("sumo_gui_settings_files"):
            self.gui_settings_files = os.path.join(
                                        self.work_dir,
                                        "gui.settings.xml"
                                    )
            file_gui = open(self.gui_settings_files, "w")
            file_gui.write(static_xml.gui_settings())
            file_gui.close()
        else :
            self.gui_settings_files = "".join(os.path.join(self.work_dir, elt)+"," for elt in self.scenario_network_config.get("sumo_gui_settings_files").split(","))[:-1]
            # print(self.scenario_sumo_gui_settings_files)

        # if not self.scenario_network_config.get("sumo_config_file"):
        #     self.scenario_sumo_config_file = "/data/model.sumocfg" 
        # else :
        #     self.scenario_sumo_config_file = self.scenario_network_config.get("sumo_config_file")

        # 2/3 Read Demand Configurations

        if not self.scenario_demand_config.get("type") :
            self.demand_type = "randomTrips" # randomTrips [default] / odTrips
        else:
            self.demand_type = self.scenario_demand_config.get("type") 


        if self.scenario_demand_config.get("sumo_taz_file") :
            self.taz_file = os.path.join(
                                    self.work_dir,
                                    self.scenario_demand_config.get("sumo_taz_file")
                            )

        if self.scenario_demand_config.get("sumo_matrix_file") :
            self.matrix_file = os.path.join(
                                    self.work_dir,
                                    self.scenario_demand_config.get("sumo_matrix_file")
                            )
            # self.od_format = "matrix"

        if self.scenario_demand_config.get("sumo_amitran_file") :
            self.amitran_file = os.path.join(
                                    self.work_dir,
                                    self.scenario_demand_config.get("sumo_amitran_file")
                            )
            # self.od_format = "amitran"

        if self.scenario_demand_config.get("vType") :
            self.vType = self.scenario_demand_config.get("vType")

        # 3/3 Read Demand Configurations

        if not self.scenario_agent_config.get("type") :
            self.agent_type = "none"
        else:
            self.agent_type = self.scenario_agent_config.get("type") 


    def get(self, property_name):
        return {
            "dir" : self.work_dir,
            "index" : self.index,
            "name" : self.name,
            "prefix" : self.prefix,
            "net_file" : self.net_file,
            "add_files" : self.additional_files,
            "gui_files" : self.gui_settings_files,
            "demand_type" : self.demand_type,
            "demand_file" : self.demand_file,
            "vType" : self.vType,
            "taz_file" : self.taz_file,
            # "od_format" : self.od_format,
            "amitran_file" : self.amitran_file,
            "matrix_file" : self.matrix_file,
            "agent_type" : self.agent_type,
            "connection" : self.connection
        }[property_name]


    def add_additional_file(self, file_name):
        if self.additional_files == "" :
            self.additional_files = file_name
        else :
            self.additional_files = self.additional_files + "," + file_name

    def add_demand(self):
        self.demand_file = os.path.join(
                                    self.work_dir,
                                    self.demand_type + ".demand.xml"
                                )
        DemandManager().get_demand(self)

        self.add_additional_file(self.demand_file)

    def init_agent(self):
        if not self.agent_type == "none":
            AgentManager().initialise_agent_for_scenario(self)

    def reg_connection(self, conn):
        self.connection = conn
        # conn.open()
        # print( "connection reged for " + str(self.index))

    def open_connection(self):
        self.connection.open()
        # pass

    def close_connection(self):
        self.connection.close()

    def step(self):
        self.connection.step()


    # def generate_trip_random(self):

class ScenarioManager:

    def __init__(self):
        self.scenario_list = []
        # self.dm = DemandManager()

    def add_scenario(self, scn):
        self.scenario_list.append(scn)

    def activate_all(self):
        print("number of scenarios: " + str(len(self.scenario_list)))
        for scn in self.scenario_list:
            scn.open_connection()

        # self.monitor = Monitor(self.scenario_list)

    def step_all(self):
        for scn in self.scenario_list:
            scn.step()

    def close_all(self):
        for scn in self.scenario_list:
            scn.close_connection()
