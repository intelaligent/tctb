#!/usr/bin/env python2
"""
@file    monitor.py
@author  Bo Gao
@date    2017-08-14
@version alpha

Demand related

Copyright (C) 2017 Transport Research Group, University of Southampton

Intersection Control Test Bed
"""

import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.autoscale(enable=True, axis='both', tight=None)
import pandas as pd
import numpy as np


class Monitor(object):
    """Monitor Interface"""

    def get_step(self):
        raise NotImplementedError( "Method get_step not implemented." )

class Monitor_Throughput_Network(Monitor):

    # def step(self, scn_list):
    #     for scn in scn_list :

    def get_step(self, scn, mon_config):
        print(scn.get("name") + "\t arrived \t" + str(scn.get("connection").traci_connection.simulation.getArrivedNumber()))
        return scn.get("connection").traci_connection.simulation.getArrivedNumber()

    # def visualise_cumulative(self, ):

class Monitor_Waiting_Time_At_Edges(Monitor):

    # def step(self, scn_list):
    #     for scn in scn_list :

    def get_step(self, scn, mon_config):
        wt = sum(
                scn.get("connection").traci_connection.edge.getWaitingTime(edge_id)
                for edge_id in mon_config.get("edge_ids").split(",")
            )
        print(scn.get("name") + "\t waiting \t" + str(wt))
        return wt


class MonitorManager:

    # # measurements
    # _throughput_network = 0

    _update_period = 30 #steps
    _current_step = 0

    _df_columns = []
    _df_dict = {}

    fig, ax = plt.subplots()

    def __init__(self, scn_list):
        self.scenario_list = scn_list
        self._df_columns = [ scn.get("name") for scn in scn_list ]

        self.monitor_config_list = []

    def add_monitor(self, monitor_config):
        self.monitor_config_list.append(monitor_config)
        # self._df_dict[monitor_config.get("name")] = pd.DataFrame(columns = self._df_columns)
        self._df_dict[monitor_config.get("name")] = None
        # self._df = pd.DataFrame(columns = self._df_columns)
        # self._df =  pd.DataFrame( [[1,2],[2,0]])
        # self._df = None
    
    def step(self):

        # collect data
        if len(self.monitor_config_list) > 0 :
            for mon_config in self.monitor_config_list :
                # new_data = [[1,2],[2,0]]
                # for ss in self.scenario_list :
                #     new_data.append(self._execute_monitor_step(mon_config, ss))
                new_data = [ self._execute_monitor_step(mon_config, ss) for ss in self.scenario_list ]
                # print("new data:")
                # print(new_data)
                # new_data = new_data.astype(np.float)
                new_df = pd.DataFrame([new_data], columns = self._df_columns)
                # print("new df:")
                # print(new_df)
                # print
                # self._df_dict[mon_config.get("name")].loc[self._current_step] = new_data 
                # self._df_dict[mon_config.get("name")].append(new_df, ignore_index=True)
                if self._df_dict[mon_config.get("name")] is None:
                    self._df_dict[mon_config.get("name")] = new_df
                else:
                    self._df_dict[mon_config.get("name")] = self._df_dict[mon_config.get("name")].append(new_df, ignore_index=True)
                # print("self._df:")
                # print(self._df_dict[mon_config.get("name")])
                print(self._df_dict[mon_config.get("name")].sum())

        self._current_step = self._current_step + 1


        # visualisation
        if self._current_step % self._update_period == 0 :
            for mon_config in self.monitor_config_list :
                if mon_config.get("name") == "throughput_network" :
                    # df = self._df_dict[mon_config.get("name")]
                    # df.sum().plot(kind='barh')
                    # plt.show(block=False)
                    
                    df = self._df_dict[mon_config.get("name")]

                    self.ax.barh( np.arange(len(self._df_columns)),
                                [ df[col].sum() for col in self._df_columns ],
                                .3, # bar_width
                                align = "center"
                        )
                    
                    self.ax.set_yticks(np.arange(len(self._df_columns)))
                    self.ax.set_yticklabels(self._df_columns)
                    # self.ax.invert_yaxis()
                    self.ax.set_xlabel("number of vehicles")
                    if mon_config.get("title") :
                        self.ax.set_title(mon_config.get("title"))
                    else :
                        self.ax.set_title(mon_config.get("name"))
                    self.ax.set_ylim([-1,len(self._df_columns)])


                    # self.fig.set_size_inches(8, 6)
                    self.fig.show()
                    self.fig.canvas.draw()

        #     self.show_plot()


    def show_final_plots(self) :
        for mon_config in self.monitor_config_list :
            # self._df_dict[mon_config.get("name")].hist()
            self._df_dict[mon_config.get("name")].plot(
                    kind = "hist",
                    title = mon_config.get("title") if mon_config.get("title") else mon_config.get("name"),
                    subplots = True

                    # color = '#00BFC4', #blue
                    # color = '#F8766D', #light pink
                    # color = 'black',
                    # sharex=True,
                    # ylim=(0,400),
                    # xlim=(0,600),
                    # sharey = True,
                    # layout = (2,1),
                    # figsize = (7,6)
                )

            # plt.ion()
            # plt.draw()
            # plt.show(block=False)
            plt.show()




        # for mon_config in self.monitor_config_list :
        #     print(self._df_dict[mon_config.get("name")])
        #     self._df_dict[mon_config.get("name")].hist()
        #     plt.show()

    def _execute_monitor_step(self, monitor_config, scn) :
        return {
            "throughput_network" : lambda scn, monitor_config : Monitor_Throughput_Network().get_step(scn,monitor_config),
            "wait_time_edges" : lambda scn, monitor_config : Monitor_Waiting_Time_At_Edges().get_step(scn,monitor_config)
        }[monitor_config.get("name")](scn, monitor_config)