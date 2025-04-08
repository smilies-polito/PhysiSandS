import sys
import os
import time
import pandas as pd
sys.path.append('../')
from simulations.start_stop_simulation import start_stop_simu, start_stop_simu_second
import math

def test_start_and_stop(num_simu, step, two_D):
    current_dir = os.getcwd()

    time_steps = []
    step_alive = []
    step_necrotic = []
    step_apoptotic = []
    T_save = []
    T_reload = []
    T_total = []
    T_main = []



    current_time = 0
    duration = 1440

    stops = []

    num_iter = math.ceil(duration/step)


    for i in range(num_iter):
        if (current_time + step) < duration:
            stops.append(current_time + step)
            current_time += step
        else: 
            stops.append(duration)

    data_to_plot_alive = []
    data_to_plot_necrotic = []
    data_to_plot_apoptotic = []

    for i in stops:
        data_to_plot_alive.append([])
        data_to_plot_necrotic.append([])
        data_to_plot_apoptotic.append([])

    for sim in range(num_simu):

        success = False

        while not success:
            try:
                time_steps_flag, step_alive_flag, step_necrotic_flag, step_apoptotic_flag, percentage_of_resistant, stable_cells = start_stop_simu(step, two_D)
                success = True
            except Exception as e:
                time.sleep(1)

        times_df = pd.read_csv('output/interesting_times.txt', sep=' ', header=None)
        T_save_flag = times_df.iloc[:,0].values.tolist()
        T_reload_flag = times_df.iloc[:,1].values.tolist()
        T_total_flag = times_df.iloc[:,2].values.tolist()
        T_main_flag= times_df.iloc[:,3].values.tolist()
        T_save.append(T_save_flag)
        T_reload.append(T_reload_flag)
        T_total.append(T_total_flag)
        T_main.append(T_main_flag)


        time_steps.append(time_steps_flag)
        step_alive.append(step_alive_flag)
        step_necrotic.append(step_necrotic_flag)
        step_apoptotic.append(step_apoptotic_flag)

        n = 0
        for stop in stops:

            index = time_steps_flag.index(stop)

            data_to_plot_alive[n].extend([step_alive_flag[index]])

            data_to_plot_necrotic[n].extend([step_necrotic_flag[index]])
            
            data_to_plot_apoptotic[n].extend([step_apoptotic_flag[index]])

            n+=1

    return data_to_plot_alive, data_to_plot_apoptotic, data_to_plot_necrotic, T_save, T_reload, T_total, T_main


def test_start_and_stop_second(num_simu, step, two_D):
    current_dir = os.getcwd()

    time_steps = []
    step_epithelial = []
    step_mesenchymal = []
    T_save = []
    T_reload = []
    T_total = []
    T_main = []
    current_time = 0
    duration = 2880

    stops = []

    num_iter = math.ceil(duration/step)


    for i in range(num_iter):
        if (current_time + step) < duration:
            stops.append(current_time + step)
            current_time += step
        else: 
            stops.append(duration)
    data_to_plot_epithelial = []
    data_to_plot_mesenchymal = []
    

    for i in stops:
        data_to_plot_epithelial.append([])
        data_to_plot_mesenchymal.append([])

    for sim in range(num_simu):
        os.chdir(current_dir)
        success = False

        while not success:
            try:
                time_steps_flag, step_epithelial_flag, step_mesenchymal_flag = start_stop_simu_second(step, two_D)
                success = True
            except Exception as e:
                time.sleep(1)

        times_df = pd.read_csv('output/interesting_times.txt', sep=' ', header=None)
        T_save_flag = times_df.iloc[:,0].values.tolist()
        T_reload_flag = times_df.iloc[:,1].values.tolist()
        T_total_flag = times_df.iloc[:,2].values.tolist()
        T_main_flag = times_df.iloc[:,3].values.tolist()

        T_save.append(T_save_flag)
        T_reload.append(T_reload_flag)
        T_total.append(T_total_flag)
        T_main.append(T_main_flag)


        time_steps.append(time_steps_flag)
        step_epithelial.append(step_epithelial_flag)
        step_mesenchymal.append(step_mesenchymal_flag)

        n = 0
        for stop in stops:

            index = time_steps_flag.index(stop)

            data_to_plot_epithelial[n].extend([step_epithelial_flag[index]])

            data_to_plot_mesenchymal[n].extend([step_mesenchymal_flag[index]])
            
            n+=1

    return data_to_plot_epithelial, data_to_plot_mesenchymal, T_save, T_reload, T_total, T_main




