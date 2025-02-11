import os
import glob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.io import loadmat
import xml.etree.ElementTree as ET
from utils.multicellDS_second import MultiCellDS_second

def conversion(output_folder, save_folder):
    # Creazione del lettore MCDS
    reader = MultiCellDS_second(output_folder=output_folder)

    # Iteratore per caricare i dati delle cellule ad ogni timestep
    df_iterator = reader.cells_as_frames_iterator()

    for (t, df_cells) in df_iterator:
        continue

    df_filtered = df_cells[['x_position', 'y_position', 'z_position', 'cell_type']].copy().rename(columns={'x_position': 'x', 'y_position': 'y', 'z_position': 'z', 'cell_type': 'type'})   

    # Dizionario di mapping
    type_mapping = {
        0: "epithelial",
        1: "mesenchymal",
    }

    # Converti i valori numerici in stringhe
    df_filtered['type'] = df_filtered['type'].map(type_mapping)

    # Plot
    df_filtered.to_csv(os.path.join(save_folder, 'cells.csv'), index=False)

    return


