import sys
import os
import time
sys.path.append('../')
from simulations.start_stop_simulation import start_stop_simu, start_stop_simu_second
import math

def test_start_and_stop(num_simu, step, two_D):
    current_dir = os.getcwd()

    time_steps = []
    step_alive = []
    step_necrotic = []
    step_apoptotic = []

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
    durations = []
    counters = []

    for i in stops:
        data_to_plot_alive.append([])
        data_to_plot_necrotic.append([])
        data_to_plot_apoptotic.append([])

    for sim in range(num_simu):

        ini = time.process_time()
        time_steps_flag, step_alive_flag, step_necrotic_flag, step_apoptotic_flag, percentage_of_resistant, stable_cells = start_stop_simu(step, two_D)
        fin = time.process_time()

        duration = fin - ini

        time_steps.append(time_steps_flag)
        step_alive.append(step_alive_flag)
        step_necrotic.append(step_necrotic_flag)
        step_apoptotic.append(step_apoptotic_flag)
        durations.append(duration)

        n = 0
        for stop in stops:

            index = time_steps_flag.index(stop)
            print(index)
            print(len(step_alive_flag))

            data_to_plot_alive[n].extend([step_alive_flag[index]])

            data_to_plot_necrotic[n].extend([step_necrotic_flag[index]])
            
            data_to_plot_apoptotic[n].extend([step_apoptotic_flag[index]])

            n+=1

    return data_to_plot_alive, data_to_plot_apoptotic, data_to_plot_necrotic, durations


def test_start_and_stop_second(num_simu, step, two_D):
    current_dir = os.getcwd()

    time_steps = []
    step_epithelial = []
    step_mesenchymal = []
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
    durations = []
    counters = []

    for i in stops:
        data_to_plot_epithelial.append([])
        data_to_plot_mesenchymal.append([])

    for sim in range(num_simu):
        os.chdir(current_dir)

        ini = time.process_time()
        time_steps_flag, step_epithelial_flag, step_mesenchymal_flag = start_stop_simu_second(step, two_D)
        fin = time.process_time()

        duration = fin - ini

        time_steps.append(time_steps_flag)
        step_epithelial.append(step_epithelial_flag)
        step_mesenchymal.append(step_mesenchymal_flag)
        durations.append(duration)

        n = 0
        for stop in stops:

            index = time_steps_flag.index(stop)

            data_to_plot_epithelial[n].extend([step_epithelial_flag[index]])

            data_to_plot_mesenchymal[n].extend([step_mesenchymal_flag[index]])
            
            n+=1

    return data_to_plot_epithelial, data_to_plot_mesenchymal, durations




