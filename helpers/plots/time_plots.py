import json
import matplotlib.pyplot as plt
import os

def time_plot(quantitative_test, quantitative_test_second, output_folder):

    # Leggere i file JSON
    with open(quantitative_test, 'r') as file:
        data1 = json.load(file)
    
    with open(quantitative_test_second, 'r') as file:
        data2 = json.load(file)
    
    # Estrarre i dati
    durations1 = data1.get('Durations', [])
    durations_start_stop1 = data1.get('Durations_Start_Stop', [])
    
    durations2 = data2.get('Durations', [])
    durations_start_stop2 = data2.get('Durations_Start_Stop', [])

    #remove the first element since the compilation is taking more time and creating an outlier
    durations2 = durations2[1:]
    durations1 = durations1[1:]
    durations_start_stop2 = durations_start_stop2[1:]
    durations_start_stop1 = durations_start_stop1[1:]
    
    # Creare i dati per il boxplot
    data = [durations1, durations_start_stop1, durations2, durations_start_stop2]
    labels = ['TNF tumor', 'TNF tumor Start&Stop', 'Cancer invasion', 'Cancer invasion Start&Stop']
    colors = ['blue', 'blue', 'red', 'red']
    
    # Creare la figura con dimensioni maggiori
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plottare il boxplot
    box = ax.boxplot(data, patch_artist=True, labels=labels)
    #ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Colorare i box
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    
    # Etichette e titolo
    ax.set_ylabel('CPU time (sec)')
    ax.set_xlabel('Test Type')
    ax.set_title('Comparison of Normal and Start and Stop CPU time')
    
    # Regolare i margini per evitare che le etichette vengano tagliate
    plt.tight_layout()
        
    # Salvare il grafico
    plt.savefig(os.path.join(output_folder, 'time_plot.png'))


if __name__ == '__main__':
    quantitative_test = '/home/danariki/OneDrive/ph.D/PoliTo/PhysiBoss2.0/addon_paper/add-on_tests/quantitative_test.json'
    quantitative_test_second = '/home/danariki/OneDrive/ph.D/PoliTo/PhysiBoss2.0/addon_paper/add-on_tests/quantitative_test_second.json'
    output_folder = '/home/danariki/OneDrive/ph.D/PoliTo/PhysiBoss2.0/addon_paper/add-on_tests/'
    time_plot(quantitative_test, quantitative_test_second, output_folder)