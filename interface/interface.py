import os
import subprocess
import xml.etree.ElementTree as ET
import shutil
import json
import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pctk import multicellds
from utils.multicellDS_second import MultiCellDS_second
sys.path.append('../')


class interface:
    def __init__(self, root_dir, json_file_path, two_D):

        # define the directory
        self.root_dir = root_dir
        self.PhysiBoSS_dir = os.path.join(root_dir, 'model')
        self.two_D = two_D

        #define the parameter dict
        self.json_file_path = json_file_path
        with open(json_file_path, 'r') as file:
            self.parameter_dict = json.load(file)
        
        if self.two_D:
            self.parameter_dict['z_min']['value'] = -10
            self.parameter_dict['z_max']['value'] = 10
            self.parameter_dict['use_2D']['value'] = 'true'
        else:
            self.parameter_dict['z_min']['value'] = -500
            self.parameter_dict['z_max']['value'] = 500
            self.parameter_dict['use_2D']['value'] = 'false'

        self.output_folder = os.path.join(self.PhysiBoSS_dir, 'output')
        self.Start_Stop_folder = os.path.join(self.PhysiBoSS_dir, 'start_and_stop_saving_files')

    def update_parameters(self, iteration):
        
        # File path for the physicell settings
        if iteration == 0:
            physicell_setting_file = os.path.join(self.root_dir, 'model/sample_projects_intracellular/boolean/spheroid_tnf_model/config/PhysiCell_settings.xml')
        else:
            physicell_setting_file = os.path.join(self.root_dir, 'model/config/PhysiCell_settings.xml')
        
        # Upload XML file
        tree = ET.parse(physicell_setting_file)
        root = tree.getroot()
        
        # Extract list of parameters to update
        parameters = list(self.parameter_dict.keys())
        
        for param in parameters:
            tags = self.parameter_dict[param]['path'].split('/')
            new_value = str(self.parameter_dict[param]['value'])

            # CASO SPECIALE: aggiorna tutti i cell_definition/intracellular/...
            if tags[:3] == ['cell_definitions', 'cell_definition', 'phenotype'] and tags[3] == 'intracellular':
                target_tag = tags[-1]  # es: bnd_filename o cfg_filename
                for cd in root.findall('.//cell_definition'):
                    phenotype = cd.find('phenotype')
                    if phenotype is not None:
                        intracellular = phenotype.find('intracellular')
                        if intracellular is not None:
                            target_element = intracellular.find(target_tag)
                            if target_element is not None:
                                target_element.text = new_value
                continue  # salta il resto del loop per questo parametro

            # Altrimenti: gestione standard
            element = root
            for tag in tags:
                if element is not None:
                    if tag == 'variable' and 'name' in self.parameter_dict[param]:
                        found = False
                        for var in element.findall(tag):
                            if var.attrib['name'] == self.parameter_dict[param]['name']:
                                element = var
                                found = True
                                break
                        if not found:
                            element = None
                            break
                    elif tag != 'variable':
                        element = element.find(tag)

            if element is not None:
                element.text = new_value

        # Salva il file alla fine
        tree.write(physicell_setting_file)
        
        return 'Settings updated succesfully!'



    def update_parameters_second(self, iteration):
        
        # File path for the Physicell settings
        if iteration == 0:
            physicell_setting_file = os.path.join(self.root_dir, 'model/sample_projects_intracellular/boolean/cancer_invasion/config/PhysiCell_settings.xml')
        else:
            physicell_setting_file = os.path.join(self.root_dir, 'model/config/PhysiCell_settings.xml')
        
        # Upload XML file
        tree = ET.parse(physicell_setting_file)
        root = tree.getroot()
        
        # Extract list of parameters to update
        parameters = list(self.parameter_dict.keys())
        
        for param in parameters:
            tags = self.parameter_dict[param]['path'].split('/')
            new_value = str(self.parameter_dict[param]['value'])

            # CASO SPECIALE: aggiorna tutti i cell_definition/intracellular/...
            if tags[:3] == ['cell_definitions', 'cell_definition', 'phenotype'] and tags[3] == 'intracellular':
                target_tag = tags[-1]  # es: bnd_filename o cfg_filename

                for cell_defs in root.findall('.//cell_definitions'):
                    for cd in cell_defs.findall('cell_definition'):
                        phenotype = cd.find('phenotype')
                        if phenotype is not None:
                            intracellular = phenotype.find('intracellular')
                            if intracellular is not None:
                                target_element = intracellular.find(target_tag)
                                if target_element is not None:
                                    target_element.text = new_value
                continue  # salta il resto del loop per questo parametro

            # Gestione standard per gli altri path
            element = root
            for tag in tags:
                if element is not None:
                    if tag == 'variable' and 'name' in self.parameter_dict[param]:
                        found = False
                        for var in element.findall(tag):
                            if var.attrib['name'] == self.parameter_dict[param]['name']:
                                element = var
                                found = True
                                break
                        if not found:
                            element = None
                            break
                    elif tag != 'variable':
                        element = element.find(tag)

            if element is not None:
                element.text = new_value

        # Salva il file alla fine
        tree.write(physicell_setting_file)
        
        return 'Settings updated succesfully!'

    
    def execute_simulation(self, iteration):
        # Change current working directory
        os.chdir(self.PhysiBoSS_dir)
        
        # Need to be updated but for now let's mantain this
        executable_file = 'spheroid_TNF_model'

        if iteration == 0:

            # Recreate output folder
            first_make_command = ["make", 'data-cleanup']
            subprocess.run(first_make_command, check=True)

            reset_make_command = ["make", 'reset']
            subprocess.run(reset_make_command, check=True)
            
            clean_make_command = ["make", 'clean']
            subprocess.run(clean_make_command, check=True)

            make_command = ["make", "physiboss-tnf-model"]
            subprocess.run(make_command, check=True)
        
            make_command = ["make"]
            subprocess.run(make_command, check=True)
        
        # Run the simulation
        execute_command = ["./" + executable_file]
        subprocess.run(execute_command, check=True) 
        
        return self.output_folder

    def execute_simulation_second(self, iteration):
        # Change current working directory
        os.chdir(self.PhysiBoSS_dir)
        
        # Need to be updated but for now let's mantain this
        executable_file = 'invasion_model'

        if iteration == 0:

            # Recreate output folder
            first_make_command = ["make", 'data-cleanup']
            subprocess.run(first_make_command, check=True)

            reset_make_command = ["make", 'reset']
            subprocess.run(reset_make_command, check=True)
            
            clean_make_command = ["make", 'clean']
            subprocess.run(clean_make_command, check=True)

            make_command = ["make", "physiboss-tutorial-invasion"]
            subprocess.run(make_command, check=True)
        
            make_command = ["make"]
            subprocess.run(make_command, check=True)
        
        # Run the simulation
        execute_command = ["./" + executable_file]
        subprocess.run(execute_command, check=True) 
        
        return self.output_folder
    
    def alive_cells(self):
        # Creating a MCDS reader
        reader = multicellds.MultiCellDS(output_folder=self.output_folder)

        # Creating an iterator to load a cell DataFrame for each stored simulation time step
        df_iterator = reader.cells_as_frames_iterator()

        step_alive = []
        step_apoptotic = []
        step_necrotic = []
        time_steps = []
        print("\n")

        for (t, df_cells) in df_iterator:
            alive = (df_cells.current_phase==14).sum()
            apoptotic = (df_cells.current_phase==100).sum()
            necrotic = (df_cells.current_phase==101).sum()
            step_alive.append(alive)
            step_apoptotic.append(apoptotic)
            step_necrotic.append(necrotic)
            time_steps.append(t)
            print(f"Total alive {alive}, necrotic {necrotic} and apoptotic {apoptotic} cells at time {t}")
        
        pos = (df_cells[['x_position', 'y_position', 'z_position', 'current_phase']].values).tolist()

        
        return time_steps, step_alive, step_apoptotic, step_necrotic, pos

    def alive_cells_second(self):

        type_mapping = {
            0: "Epithelial",
            1: "Mesenchymal",
        }

        # Creazione del lettore MCDS
        reader = MultiCellDS_second(output_folder=self.output_folder)

        # Iteratore per caricare i dati delle cellule ad ogni timestep
        df_iterator = reader.cells_as_frames_iterator()

        # Creiamo una cartella per salvare le immagini
        output_images_folder = os.path.join(self.output_folder, "cell_plots")
        os.makedirs(output_images_folder, exist_ok=True)

        step_epithelial = []
        step_mesenchymal = []
        time_steps = []

        for (t, df_cells) in df_iterator:
            cell_types = df_cells["cell_type"]

            epithelial = (cell_types == 0).sum()
            mesenchymal = (cell_types == 1).sum()

            step_epithelial.append(epithelial)
            step_mesenchymal.append(mesenchymal)
            time_steps.append(t)
            print(f"Total epithelial {epithelial} and mesenchymal {mesenchymal} cells at time {t}")

        return time_steps, step_epithelial, step_mesenchymal


    def plot(self, time_steps, step_alive, step_necrotic, step_apoptotic, pos, resistance=False, stop_time=None):
        # Use Set1 colormap for colors
        cmap = plt.get_cmap('Set1')
        color_alive = cmap(0)
        color_necrotic = cmap(1)
        color_apoptotic = cmap(2)
        color_resistant = cmap(3)  # Only used if resistance is True

        # Plotting the data
        fig, ax = plt.subplots(figsize=(10, 6))

        if resistance:
            df = pd.read_csv('../model/output/resistant_cells.txt', header=None)
            resistant_cells = df.values.flatten().tolist()
            print(len(resistant_cells))

            # Create stackplot with resistance
            ax.stackplot(time_steps, list(np.array(step_alive)-np.array(resistant_cells)), resistant_cells, step_necrotic, step_apoptotic, colors=[color_alive, color_resistant, color_necrotic, color_apoptotic], labels=['Alive Cells', 'Resistant Cells', 'Necrotic Cells', 'Apoptotic Cells'])
        else:
            # Create stackplot without resistance
            ax.stackplot(time_steps, step_alive, step_necrotic, step_apoptotic, colors=[color_alive, color_necrotic, color_apoptotic], labels=['Alive Cells', 'Necrotic Cells', 'Apoptotic Cells'])

        if stop_time is not None:
            ax.axvline(x=stop_time, color='black', linestyle='--', label='Stop Time')

        # Increase font size and use Set1 colormap
        ax.set_xlabel('Time (min)', fontsize=14)
        ax.set_ylabel('Number of Cells', fontsize=14)
        ax.set_title('Cell Population over Time', fontsize=16)
        ax.set_xticks([0, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350])
        ax.tick_params(axis='both', which='major', labelsize=15)
        ax.legend(fontsize=15)
        ax.grid(True)

        plt.savefig(os.path.join(self.output_folder, 'cell_population_over_time.pdf'))

    def plot_second(self, time_steps, epithelial_step, mesenchymal_step, stop_time=None):
        # Use Set1 colormap for colors
        cmap = plt.get_cmap('Set1')
        color_epithelial = 'red'  # Epithelial Cells
        color_mesenchymal = 'green'  # Mesenchymal Cells

        # Plotting the data
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create stackplot for epithelial and mesenchymal cells only
        ax.stackplot(
            time_steps,
            epithelial_step,
            mesenchymal_step,
            colors=[color_epithelial, color_mesenchymal],
            labels=['Epithelial Cells', 'Mesenchymal Cells']
        )

        if stop_time is not None:
            ax.axvline(x=stop_time, color='black', linestyle='--', label='Stop Time')

        # Formatting
        ax.set_xlabel('Time (min)', fontsize=14)
        ax.set_ylabel('Number of Cells', fontsize=14)
        ax.set_title('Epithelial vs. Mesenchymal Cell Population Over Time', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=15)
        ax.legend(loc='upper left', fontsize=15)
        ax.grid(True)

        # Save the plot
        plt.savefig(os.path.join(self.output_folder, 'epithelial_mesenchymal_population.pdf'))
        plt.close()
    
    def resistance_detection(self, alive_cells):

        
        stable_states = ['TNF TNFR RIP1 RIP1ub RIP1K IKK NFkB BCL2 ATP cIAP XIAP cFLIP Survival',
                        'FASL TNF TNFR RIP1 RIP1ub RIP1K IKK NFkB BCL2 ATP cIAP XIAP cFLIP Survival',
                        'TNF TNFR DISC-TNF FADD RIP1 RIP1ub RIP1K IKK NFkB BCL2 ATP cIAP XIAP cFLIP Survival',
                        'FASL DISC-FAS FADD RIP1 RIP1ub RIP1K IKK NFkB BCL2 ATP cIAP XIAP cFLIP Survival',
                        'FASL TNF TNFR DISC-TNF DISC-FAS FADD RIP1 RIP1ub RIP1K IKK NFkB BCL2 ATP cIAP XIAP cFLIP Survival']
        for i in range(len(stable_states)):
            stable_states[i] = stable_states[i].split(' ')

        # read the bool_data.txt file
        filename = os.path.join(self.PhysiBoSS_dir, 'starting_file_trial/bool_data.txt')
        command = ["awk", "{print}", filename]
        result = subprocess.run(command, capture_output=True, text=True)
        lines = result.stdout.split('\n')[:-1]

        counter_stable = 0
        for raw_line in lines:
            raw_line = raw_line.split(' ')
            line = []
            for i in range(len(raw_line)-1):
                flag = raw_line[i].replace(";", "").split('=')
                node = flag[0]
                value = flag[1]

                if value == '1':
                    line.append(node)

            for state in stable_states:
                if set(state).issubset(set(line)):
                    counter_stable += 1
                    break  # exit the inner loop if a match is found

        percentage_of_resistant = counter_stable/alive_cells
        
        return percentage_of_resistant, counter_stable



