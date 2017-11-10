#!/usr/bin/env python2
"""
@file    simulation.py
@author  Bo Gao
@date    2017-07-25
@version alpha

Core module of Intersection Control Test Bed

Copyright (C) 2017 Transport Research Group, University of Southampton

Core module of Intersection Control Test Bed
"""
import os
import sys
import signal

import argparse

import datetime
from distutils.dir_util import copy_tree

import xml.etree.ElementTree as ET

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
    import randomTrips
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

from classes.connection import ConnectionManager
from classes.scenario import Scenario, ScenarioManager
from classes.monitor import MonitorManager

import classes.static_xml as static_xml


def init_args():
    parser = argparse.ArgumentParser(description="Execute SUMO simulations in parallel.")
    # parser.add_argument("-o", "--outname", type=str, help="name used for the generated network")
    parser.add_argument("-c", "--configfile", type=str, help="name of simulation configuration file")
    parser.add_argument("-w", "--workspace", type=str, help="work directory")
    
    use_gui_parser = parser.add_mutually_exclusive_group(required=False)
    use_gui_parser.add_argument("--gui", dest="use_gui", action="store_true", help="default, invoke sumo-gui binary")
    use_gui_parser.add_argument("--no-gui", dest="use_gui", action="store_false", help="invoke sumo binary")

    parser.set_defaults(configfile="./demo_configs/demo.sim_config.xml", workspace="./workspace", use_gui=True)
    args = parser.parse_args()
    return args


def early_exit_handler(signal, frame):

    print("Simulation exited by Ctrl+C")
    mm.show_plot()
    raw_input("Press ENTER to exit.")

    sm.close_all()
    sys.exit(0)


def run():
    sim_steps_count = 0

    while (sim_steps_count < sim_steps_total):

        # cm.step_all()
        sm.step_all()

        mm.step()

        sim_steps_count = sim_steps_count + 1

        # print("step: " + str(sim_steps_count) + "/" + str(sim_steps_total) + "\n")

if __name__ == "__main__":

    args = init_args()

    if args.use_gui:
        ConnectionManager.sumo_binary = ConnectionManager.SUMO_BINARY_GUI #"sumo-gui"
    else:
        ConnectionManager.sumo_binary = ConnectionManager.SUMO_BINARY_COMMAND_LINE #"sumo"

    # read simulation configuration xml
    sim_config_tree = ET.parse(args.configfile)
    sim_config_root = sim_config_tree.getroot()

    # create sub directory in a workspace directory
    if not os.path.exists(args.workspace):
        os.makedirs(args.workspace)

    sim_dir = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = os.path.join(args.workspace, sim_dir)
    os.makedirs(work_dir)


    # initialise and configure each scenario
    cm = ConnectionManager()
    # dm = DemandManager()
    sm = ScenarioManager()

    ii = 0
    for scn_config in sim_config_root.findall("scenario"):

        # Copy model files to workspace
        scenario_dir = os.path.join(work_dir, "scenario" + str(ii))
        copy_tree(scn_config.find("network").get("path"), scenario_dir)

        # Write common additional files
        add_vTypes_file = os.path.join(
                                    scenario_dir,
                                    "add.vTypes.xml"
                                )
        file_add_vTypes = open(add_vTypes_file, "w")
        file_add_vTypes.write(static_xml.vTypes_file())
        file_add_vTypes.close()

        add_dumps_file = os.path.join(
                                    scenario_dir,
                                    "add.dumps.xml"
                                )
        file_add_dumps = open(add_dumps_file, "w")
        file_add_dumps.write(static_xml.dump_file(scenario_dir))
        file_add_dumps.close()


        # Configure a scenario
        scn = Scenario(scenario_dir, scn_config, ii)

        scn.add_additional_file(add_vTypes_file)
        scn.add_additional_file(add_dumps_file)

        scn.add_demand() # mandatory, prior to agent init

        scn.init_agent() # mandatory, prior to agent activate

        # need to hand this to Scenario class
        conn = cm.reg_connection(
            scn.get("dir"),
            scn.get("net_file"),
            scn.get("add_files"),
            scn.get("gui_files")
        )

        scn.reg_connection(conn)

        print("scenario " + str(ii) + " initilised")

        sm.add_scenario(scn)

        ii = ii + 1

    # cm.open_all()
    sm.activate_all()




    mm = MonitorManager(sm.scenario_list)

    if sim_config_root.findall("monitor") :
        for monitor_config in sim_config_root.findall("monitor"):
            mm.add_monitor(monitor_config)


    if not sim_config_root.get("steps"):
        sim_steps_total = 2000 # default
    else:
        sim_steps_total = int(sim_config_root.get("steps"))

    print("total number of steps:" + str(sim_steps_total))


    # simulation start

    # signal.signal(signal.SIGINT, early_exit_handler)

    run()

    mm.show_final_plots()

    for monitor_name, data in mm._df_dict.iteritems():
        data.to_csv(work_dir + "/monitor_df_" + monitor_name + ".csv", sep = " ")

    sys.stdout.flush()


    # cm.close_all()
    sm.close_all()
    

    # Create symlink to the latest results
    latest_link = os.path.join(args.workspace,"latest")
    latest_target = sim_dir

    if not os.path.exists(latest_link) :
        os.symlink(latest_target, latest_link)
    else :
        os.remove(latest_link)
        os.symlink(latest_target, latest_link)

    print("simulation finished\n")