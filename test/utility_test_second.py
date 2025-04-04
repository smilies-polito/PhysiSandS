import sys
import argparse
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('../')
from interface.interface import interface
from simulations.single_simulation import single_simu_second
from utils.conv import conversion

def convert_int64(obj):
    if isinstance(obj, dict):
        return {k: convert_int64(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_int64(v) for v in obj]
    elif isinstance(obj, np.int64):
        return int(obj)
    else:
        return obj

def create_combined_stackplot(output_dir):
    # Leggi il file JSON
    with open(f"{output_dir}/qualitative_test_second.json", 'r') as file:
        data = json.load(file)
    
    # Estrai i dati dal file JSON
    time_steps_tot = data['time_steps_tot']
    step_epithelial_tot = data['step_epithelial_tot']
    step_mesenchymal_tot = data['step_mesenchymal_tot']
    stop_times = data['stop_times']

    # Usa la colormap Set1 per i colori
    cmap = plt.get_cmap('Set1')
    color_epithelial = cmap(4)
    color_mesenchymal = cmap(1)

    # Crea la figura per contenere i subplot
    fig, axs = plt.subplots(2, 1, figsize=(6, 10))  # Dimensioni modificate per adattare i subplot

    # Definisci i titoli per ogni subplot
    titles = ['Continuous Simulation', 'Start-Stop Simulation']
    letters = ['a', 'b']  # Lettere per ogni subplot

    # Loop attraverso ogni subplot e plotta i dati
    for i, ax in enumerate(axs.flat):
        if stop_times[i] is not None:
            ax.axvline(x=stop_times[i], color='r', linestyle='--', label='Stop Time')
        ax.stackplot(time_steps_tot[i], step_epithelial_tot[i],  step_mesenchymal_tot[i], 
                     colors=[color_epithelial, color_mesenchymal], 
                     labels=['epithelial Cells', 'mesenchymal Cells'])
            
        # Imposta il titolo e regola il layout
        ax.set_title(f"{letters[i]}) {titles[i]}", fontsize=10, fontweight='bold')  # Includi la lettera nel titolo
        ax.set_xlabel('Time (min)', fontsize=10)
        ax.set_ylabel('Number of Cells', fontsize=10)
        ax.set_xticks([0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700])
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{output_dir}/combined_stackplot_second.pdf")
    plt.close()
    print(stop_times)


def qualitative_test(output_dir):
    # Set the root dir
    os.chdir('..')
    root_dir = os.getcwd()

    # set the 2 D
    two_D = True
    # ----------------------------------------#
    # CONTINUOUS SIMULATION epithelial CELLS
    # Read the json file to set the parameters, made this way to reuse the interface
    json_file_path = 'helpers/simulation_parameters/simulation_parameters_second.json'
    with open(json_file_path, 'r') as file:
        parameter_dict = json.load(file)

    # update parameters according to the current ideal simulation
    parameter_dict['auto_stop']['value'] = 'false'
    parameter_dict['start_stop']['value'] = 'false'
    parameter_dict['auto_stop']['value'] = 'false'
    parameter_dict['initial_conditions']['value'] = './config'
    parameter_dict['SRC_cfg']['value'] = "config/boolean_network/intracellular_model.cfg"
    parameter_dict['SRC_bnd']['value'] = "config/boolean_network/intracellular_model.bnd"

    #update the json file
    with open(json_file_path, 'w') as file:
        json.dump(parameter_dict, file, indent=4)

    #execute the first simulation with initial parameters
    time_steps_cont, step_epithelial_cont, step_mesenchymal_cont = single_simu_second(two_D)

    # ----------------------------------------#
    # START STOP SIMULATION epithelial CELLS
    # update the parameters for the second simulation
    os.chdir('..')
    parameter_dict['auto_stop']['value'] = 'true'

    #update the json file
    with open(json_file_path, 'w') as file:
        json.dump(parameter_dict, file, indent=4)

    #run the first simulation until it auto stops
    json_file_path = os.path.join(root_dir, json_file_path)

    # define interface object
    my_interface = interface(root_dir, json_file_path, two_D)

    # update_parameters_second
    iteration = 0

    my_interface.update_parameters_second(iteration)

    # Execute the simulation with new parameters

    output_folder = my_interface.execute_simulation_second(iteration)

    time_steps_ss, step_epithelial_ss, step_mesenchymal_ss = my_interface.alive_cells_second()

    # Set parameters for the plot
    stop_time = time_steps_ss[-1]

    # update the parameters
    parameter_dict['start_stop']['value'] = 'true'
    conversion(my_interface.output_folder, my_interface.Start_Stop_folder)
    parameter_dict['initial_conditions']['value'] = './start_and_stop_saving_files'
    parameter_dict['auto_stop']['value'] = 'false'
    parameter_dict['SRC_cfg']['value'] = "config/boolean_network/intracellular_model_SRC.cfg"
    parameter_dict['SRC_bnd']['value'] = "config/boolean_network/intracellular_model_SRC.bnd"

    #update the json file
    with open(json_file_path, 'w') as file:
        json.dump(parameter_dict, file, indent=4)

    #run the second simulation until the end
    # define interface object
    my_interface = interface(root_dir, json_file_path, two_D)

    # update_parameters_second
    iteration = 1

    my_interface.update_parameters_second(iteration)

    # Execute the simulation with new parameters

    output_folder = my_interface.execute_simulation_second(iteration)

    # Count epithelial cells for iteration and plot
    time_steps_ss, step_epithelial_ss, step_mesenchymal_ss = my_interface.alive_cells_second()

    data = {
        "time_steps_tot": [list(time_steps_cont), list(time_steps_ss)],
        "step_epithelial_tot": [list(step_epithelial_cont), list(step_epithelial_ss)],
        "step_mesenchymal_tot": [list(step_mesenchymal_cont), list(step_mesenchymal_ss)],
        "stop_times": [None, stop_time],
    }
    data = convert_int64(data)

    
    # save the file
    with open(f"{output_dir}/qualitative_test_second.json", 'w') as file:
        json.dump(data, file, indent=4)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run qualitative test with specified output directory.')
    parser.add_argument('output_dir', type=str, help='The output directory')

    args = parser.parse_args()

    qualitative_test(args.output_dir)

    create_combined_stackplot(args.output_dir)
