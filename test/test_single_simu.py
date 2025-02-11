import sys
import os
import time
import json
sys.path.append('../')
from simulations.single_simulation import single_simu, single_simu_second


import math

def test_single_simu(num_simu, step, two_D, resistance=False):
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

    #modify the parameters according to the simulation we want to build

    json_file_path = 'helpers/simulation_parameters/simulation_parameters.json'
    with open(json_file_path, 'r') as file:
        parameter_dict = json.load(file)

    # update parameters according to the current ideal simulation
    parameter_dict['auto_stop']['value'] = 'false'
    parameter_dict['start_stop']['value'] = 'false'
    parameter_dict['read_init']['value'] = 'false'
    parameter_dict['auto_stop_resistance']['value'] = 'false'
    parameter_dict['tnf_pulse_concentration']['value'] = 0.005
    parameter_dict['tnf_pulse_duration']['value'] = 10
    parameter_dict['tnf_pulse_period']['value'] = 150
    parameter_dict['if_start_inj']['value'] = 'true'

    with open(json_file_path, 'w') as file:
        json.dump(parameter_dict, file, indent=4)

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
        if sim != 0:
            os.chdir('..')
        ini = time.process_time()
        time_steps_flag, step_alive_flag, step_necrotic_flag, step_apoptotic_flag, pos, percentage_of_resistant, stable_cells  = single_simu(two_D, resistance=resistance)
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

            data_to_plot_alive[n].extend([step_alive_flag[index]])

            data_to_plot_necrotic[n].extend([step_necrotic_flag[index]])
            
            data_to_plot_apoptotic[n].extend([step_apoptotic_flag[index]])

            n+=1

    return data_to_plot_alive, data_to_plot_apoptotic, data_to_plot_necrotic, durations

def test_single_simu_second(num_simu, step, two_D, resistance=False):
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

    #modify the parameters according to the simulation we want to build

    json_file_path = 'helpers/simulation_parameters/simulation_parameters_second.json'
    with open(json_file_path, 'r') as file:
        parameter_dict = json.load(file)

    # update parameters according to the current ideal simulation
    parameter_dict['start_stop']['value'] = 'false'
    parameter_dict['initial_conditions']['value'] = './config'

    with open(json_file_path, 'w') as file:
        json.dump(parameter_dict, file, indent=4)

    data_to_plot_epithelial = []
    data_to_plot_mesenchymal = []
    durations = []
    counters = []

    for i in stops:
        data_to_plot_epithelial.append([])
        data_to_plot_mesenchymal.append([])

    for sim in range(num_simu):
        if sim != 0:
            os.chdir('..')
        ini = time.process_time()
        time_steps_flag, step_epithelial_flag, step_mesenchymal_flag = single_simu_second(two_D)
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
