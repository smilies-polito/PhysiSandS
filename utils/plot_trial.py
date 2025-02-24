import os
import glob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.io import loadmat
import xml.etree.ElementTree as ET
from multicellDS_second import MultiCellDS_second

def alive_cells_second(output_folder):

        type_mapping = {
            0: "Epithelial",
            1: "Mesenchymal",
        }

        # Creazione del lettore MCDS
        reader = MultiCellDS_second(output_folder=output_folder)

        # Iteratore per caricare i dati delle cellule ad ogni timestep
        df_iterator = reader.cells_as_frames_iterator()

        # Creiamo una cartella per salvare le immagini
        output_images_folder = os.path.join(output_folder, "cell_plots")
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

def plot_second(output_folder, time_steps, epithelial_step, mesenchymal_step, stop_time=None):
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
        plt.savefig(os.path.join(output_folder, 'epithelial_mesenchymal_population.pdf'))
        plt.close()
    

if __name__ == '__main__':
    output_folder = '../model/output'
    time_steps, epithelial_step, mesenchymal_step = alive_cells_second(output_folder)
    plot_second(output_folder, time_steps, epithelial_step, mesenchymal_step)
