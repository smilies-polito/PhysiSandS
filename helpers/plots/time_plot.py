import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def compute_mean_std(data, axis):
    data_array = np.array(data) 
    mean_values = np.mean(data_array, axis=axis)
    std_values = np.std(data_array, axis=axis) 
    return mean_values.tolist(), std_values.tolist()

def time_plot(quantitative_test, output_folder):

    # Leggere i file JSON
    with open(quantitative_test, 'r') as file:
        data1 = json.load(file)

    # getting times from the single simulation
    T_total_continuous = data1['T_total']
    T_total_continuous_mean = np.mean(T_total_continuous)
    print(T_total_continuous_mean)
    T_total_continuous_std = np.std(T_total_continuous)

    # getting times from the start and stop simulation
    T_save_ss = data1['T_save_ss']
    T_reload_ss = data1['T_reload_ss']
    T_total_ss = data1['T_total_ss']
    T_main_ss = data1['T_main_ss']
    time_steps = [0, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1440]

    mean_T_save, std_T_save = compute_mean_std(T_save_ss, 0)
    mean_T_reload, std_T_reload = compute_mean_std(T_reload_ss, 0)
    mean_T_total, std_T_total = compute_mean_std(T_total_ss, 0)
    print(np.sum(mean_T_total))
    mean_T_main, std_T_main = compute_mean_std(T_main_ss, 0)

    # getting cells from the start and stop simulation
    alive_ss = data1['Alive_Start_Stop']
    necrotic_ss = data1['Necrotic_Start_Stop']
    apoptotic_ss = data1['Apoptotic_Start_Stop']
    total_cells = list(np.array(alive_ss) + np.array(necrotic_ss) + np.array(apoptotic_ss))
    

    mean_alive, std_alive = compute_mean_std(alive_ss, 1)
    mean_necrotic, std_necrotic = compute_mean_std(necrotic_ss, 1)
    mean_apoptotic, std_apoptotic = compute_mean_std(apoptotic_ss, 1) 
    mean_total, std_total = compute_mean_std(total_cells, 1)
    mean_total = [125] + mean_total

    # Creazione della figura e dell'asse principale
    fig, ax = plt.subplots(figsize=(10, 6))

    # Definire i colori per le barre
    colors = ['blue', 'orange', 'red']
    labels = ['T_main', 'T_Reload', 'T_Save']

    # Creare un asse X equispaziato con 11 valori, incluso 125
    x_positions = np.linspace(1, len(time_steps), len(time_steps))  # 11 valori equispaziati

    # Plot delle barre tra ogni coppia di valori consecutivi con i tempi reali (non scalati)
    for i in range(len(time_steps)-1):
        x_start = x_positions[i]
        x_end = x_positions[i + 1]

        # Valori reali dei tempi
        y_main = mean_T_main[i]
        y_reload = mean_T_main[i] + mean_T_reload[i]
        y_save = mean_T_main[i] + mean_T_reload[i] + mean_T_save[i]

        # Disegna il riquadro per i tre tipi di tempo
        ax.fill_between([x_start, x_end], 0, y_main, color=colors[0], alpha=0.8, label=labels[0] if i == 0 else "")
        ax.fill_between([x_start, x_end], y_main, y_reload, color=colors[1], alpha=0.8, label=labels[1] if i == 0 else "")
        ax.fill_between([x_start, x_end], y_reload, y_save, color=colors[2], alpha=0.8, label=labels[2] if i == 0 else "")

    # Configurare l'asse X principale (Simulated Time)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f"{val}" for val in time_steps])
    ax.set_xlabel("Simulated Time (min)")
    ax.set_ylabel("CPU Time (s)")
    ax.set_title("CPU Time for Different Start-Stop Phases - TNF Tumor")
    ax.legend()

    # Creare un secondo asse X sopra per il numero di cellule iniziale
    ax_top = ax.twiny()  # Crea un asse X superiore
    ax_top.set_xlim(ax.get_xlim())
    ax_top.set_xticks(x_positions)  # Stessi punti di riferimento dell'asse inferiore
    ax_top.set_xticklabels([f"{int(val)}" for val in mean_total])  # Mostra il numero di cellule iniziale
    ax_top.set_xlabel("Number of Cells")  # Etichetta dell'asse superiore

    plt.savefig(os.path.join(output_folder, 'time_plot_main.pdf'), bbox_inches='tight')
    plt.close()

def time_plot_second(quantitative_test, output_folder):

    # Leggere i file JSON
    with open(quantitative_test, 'r') as file:
        data1 = json.load(file)

    # getting times from the single simulation
    T_total_continuous = data1['T_total']
    T_total_continuous_mean = np.mean(T_total_continuous)
    print(T_total_continuous_mean)
    T_total_continuous_std = np.std(T_total_continuous)

    # getting times from the start and stop simulation
    T_save_ss = data1['T_save_ss']
    T_reload_ss = data1['T_reload_ss']
    T_total_ss = data1['T_total_ss']
    T_main_ss = data1['T_main_ss']
    time_steps = [0, 600, 1200, 1800, 2400, 2880]

    mean_T_save, std_T_save = compute_mean_std(T_save_ss, 0)
    mean_T_reload, std_T_reload = compute_mean_std(T_reload_ss, 0)
    mean_T_total, std_T_total = compute_mean_std(T_total_ss, 0)
    print(np.sum(mean_T_total))
    mean_T_main, std_T_main = compute_mean_std(T_main_ss, 0)

    # getting cells from the start and stop simulation
    epithelial_ss = data1['epithelial_Start_Stop']
    mesenchymal_ss = data1['mesenchymal_Start_Stop']
    total_cells = list(np.array(epithelial_ss) + np.array(mesenchymal_ss))
    

    mean_alive, std_alive = compute_mean_std(epithelial_ss, 1)
    mean_necrotic, std_necrotic = compute_mean_std(mesenchymal_ss, 1)
    mean_total, std_total = compute_mean_std(total_cells, 1)
    mean_total = [123] + mean_total

    # Creazione della figura e dell'asse principale
    fig, ax = plt.subplots(figsize=(10, 6))

    # Definire i colori per le barre
    colors = ['blue', 'orange', 'red']
    labels = ['T_main', 'T_Reload', 'T_Save']

    # Creare un asse X equispaziato con 11 valori, incluso 125
    x_positions = np.linspace(1, len(time_steps), len(time_steps))  # 11 valori equispaziati

    # Plot delle barre tra ogni coppia di valori consecutivi con i tempi reali (non scalati)
    for i in range(len(time_steps) - 1):
        x_start = x_positions[i]
        x_end = x_positions[i + 1]

        # Valori reali dei tempi
        y_main = mean_T_main[i]
        y_reload = mean_T_main[i] + mean_T_reload[i]
        y_save = mean_T_main[i] + mean_T_reload[i] + mean_T_save[i]

        # Disegna il riquadro per i tre tipi di tempo
        ax.fill_between([x_start, x_end], 0, y_main, color=colors[0], alpha=0.8, label=labels[0] if i == 0 else "")
        ax.fill_between([x_start, x_end], y_main, y_reload, color=colors[1], alpha=0.8, label=labels[1] if i == 0 else "")
        ax.fill_between([x_start, x_end], y_reload, y_save, color=colors[2], alpha=0.8, label=labels[2] if i == 0 else "")

    # Configurare l'asse X principale (Simulated Time)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f"{val}" for val in time_steps])
    ax.set_xlabel("Simulated Time (min)")
    ax.set_ylabel("CPU Time (s)")
    ax.set_title("CPU Time for Different Start-Stop - Cancer Invasion")
    ax.legend()

    # Creare un secondo asse X sopra per il numero di cellule iniziale
    ax_top = ax.twiny()  # Crea un asse X superiore
    ax_top.set_xlim(ax.get_xlim())
    ax_top.set_xticks(x_positions)  # Stessi punti di riferimento dell'asse inferiore
    ax_top.set_xticklabels([f"{int(val)}" for val in mean_total])  # Mostra il numero di cellule iniziale
    ax_top.set_xlabel("Number of Cells")  # Etichetta dell'asse superiore

    plt.savefig(os.path.join(output_folder, 'time_plot_main_second.pdf'), bbox_inches='tight')
    plt.close()




if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <quantitative_test.json> <quantitative_test_second.json>  <output_folder>")
        sys.exit(1)

    quantitative_test = sys.argv[1]
    quantitative_test_second = sys.argv[2]
    output_folder = sys.argv[3]
    
    time_plot(quantitative_test, output_folder)
    time_plot_second(quantitative_test_second, output_folder)