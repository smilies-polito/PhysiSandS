import sys
import os
import math
sys.path.append('../')
from interface.interface import interface
from utils.conv import conversion

def start_stop_simu(step, two_D):
    os.chdir('..')
    root_dir = os.getcwd()
    json_file_path = os.path.join(root_dir, 'helpers/simulation_parameters/simulation_parameters.json')

    # define interface object
    my_interface = interface(root_dir, json_file_path, two_D)
    duration = my_interface.parameter_dict['max_time']['value']
    num_iter = math.ceil(duration/step)

    # define current time
    current_time = 0

    # define usefull lists
    step_alive = []
    step_apoptotic = []
    step_necrotic = []
    time_steps = []

    # Execute the simulation with new parameters
    for iteration in range(num_iter):

        # here we will put the function that calls the reinforcement learning and updates the parameters in the correct way

        if iteration == 0:
            my_interface.parameter_dict['read_init']['value'] = 'false'
            my_interface.parameter_dict['max_time']['value'] = step
            current_time += step
        else:
            my_interface.parameter_dict['seed_tnf']['value'] = 'false'
            my_interface.parameter_dict['start_stop']['value'] = 'true'
            if (current_time + step) < duration:
                my_interface.parameter_dict['read_init']['value'] = 'true'
                my_interface.parameter_dict['if_start_inj']['value'] = 'true'
                current_time += step
                my_interface.parameter_dict['max_time']['value'] = current_time
            else:
                my_interface.parameter_dict['read_init']['value'] = 'true'
                my_interface.parameter_dict['if_start_inj']['value'] = 'true'
                current_time = duration
                my_interface.parameter_dict['max_time']['value'] = duration
                


        # Call update parameters function
        my_interface.update_parameters(iteration)


        # execute simulation
        output_folder = my_interface.execute_simulation(iteration)

    # Count alive cells for iteration and plot
    time_steps_flag, step_alive_flag, step_apoptotic_flag, step_necrotic_flag, pos = my_interface.alive_cells()

    # Execute plot
    my_interface.plot(time_steps_flag, step_alive_flag, step_necrotic_flag, step_apoptotic_flag, pos)

    # evaluate resistance
    percentage_of_resistant, stable_cells = my_interface.resistance_detection(step_alive_flag[-1])
    
    return time_steps_flag, step_alive_flag, step_necrotic_flag, step_apoptotic_flag, percentage_of_resistant, stable_cells

def start_stop_simu_second(step, two_D):
    os.chdir('..')
    root_dir = os.getcwd()
    json_file_path = os.path.join(root_dir, 'helpers/simulation_parameters/simulation_parameters_second.json')

    # define interface object
    my_interface = interface(root_dir, json_file_path, two_D)
    duration = my_interface.parameter_dict['max_time']['value']
    num_iter = math.ceil(duration/step)

    # define current time
    current_time = 0

    # Execute the simulation with new parameters
    for iteration in range(num_iter):

        # here we will put the function that calls the reinforcement learning and updates the parameters in the correct way

        if iteration == 0:
            my_interface.parameter_dict['max_time']['value'] = step
            my_interface.parameter_dict['start_stop']['value'] = 'false'
            my_interface.parameter_dict['initial_conditions']['value'] = './config'
            current_time += step
        else:
            conversion(my_interface.output_folder, my_interface.Start_Stop_folder)
            my_interface.parameter_dict['initial_conditions']['value'] = './start_and_stop_saving_files'
            my_interface.parameter_dict['start_stop']['value'] = 'true'
            if (current_time + step) < duration:
                current_time += step
                my_interface.parameter_dict['max_time']['value'] = current_time
            else:
                current_time = duration
                my_interface.parameter_dict['max_time']['value'] = duration
                

        # save the parameters

        # Call update parameters function
        my_interface.update_parameters_second(iteration)

        output_folder = my_interface.execute_simulation_second(iteration)

    # Count alive cells for iteration and plot
    time_steps_flag, step_epithelial_flag, step_mesenchymal_flag = my_interface.alive_cells_second()

    # Execute plot
    my_interface.plot_second(time_steps_flag, step_epithelial_flag, step_mesenchymal_flag)
    
    return time_steps_flag, step_epithelial_flag, step_mesenchymal_flag

if __name__ == "__main__":
    step = 600
    two_D = True
   # time_steps, step_epithelial, step_mesenchymal  = start_stop_simu_second(step, two_D)
    start_stop_simu(step, two_D)