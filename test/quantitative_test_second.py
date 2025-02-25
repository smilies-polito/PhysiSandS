import os
import argparse
import json
from test_single_simu import test_single_simu_second
from test_start_stop import test_start_and_stop_second
import numpy as np
import matplotlib.pyplot as plt

def convert_int64(obj):
    if isinstance(obj, dict):
        return {k: convert_int64(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_int64(v) for v in obj]
    elif isinstance(obj, np.int64):
        return int(obj)
    else:
        return obj

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Parameters:
    - color: The color to lighten
    - amount: The amount to lighten the color. 0 will be the original color, 1 will be white.

    Returns:
    - Lightened color
    """
    import matplotlib.colors as mc

def create_combined_boxplots(output_dir):
    # Load the data from the JSON file
    with open(os.path.join(output_dir, 'quantitative_test_second.json'), 'r') as f:
        data = json.load(f)

    # Extract the data for each category
    epithelial = data['epithelial']
    mesenchymal = data['mesenchymal']
    epithelial_s_s = data['epithelial_Start_Stop']
    mesenchymal_s_s = data['mesenchymal_Start_Stop']

    # Define the categories for the boxplots
    categories = ['epithelial', 'mesenchymal']
    letters = ['a', 'b']
    # Get a color map to use different colors for each category
    cmap = plt.get_cmap('Set1')
    colors = ['red', 'green']

    # Define the x-axis values (time steps in minutes)
    x_values = [600, 1200, 1800, 2400, 2880]

    # Create a figure and a set of subplots (one for each category)
    fig, axs = plt.subplots(2, 1, figsize=(5, 8))  # Reduced the size
    # Set the main title of the figure
    fig.suptitle('Comparison between Normal and Start-Stop Simulation', fontsize=10)  # Reduced font size

    # Define the x-axis positions as sequential integer values
    x_positions = list(range(len(x_values)))

    for i, ax in enumerate(axs):
        # Get the current category and the corresponding data
        category = categories[i]
        data_normal = eval(category.lower())
        data_s_s = eval(category.lower() + '_s_s')

        # Prepare the data to be plotted for both normal and start-stop simulations
        data_to_plot_normal = [data_normal[j] for j in range(len(x_values))]
        data_to_plot_s_s = [data_s_s[j] for j in range(len(x_values))]

        print(len(data_normal))

        # Store the boxplot elements to use in the legend
        boxplot_elements = []

        for j in range(len(x_values)):
            # Plot the boxplots using the integer positions on the x-axis
            # Adjust the positions to place the boxplots side by side
            bp_normal = ax.boxplot(data_to_plot_normal[j], positions=[x_positions[j] - 0.2], widths=0.3, patch_artist=True, boxprops=dict(facecolor=colors[i]))
            lighter_color = lighten_color(colors[i], amount=0.3)
            bp_s_s = ax.boxplot(data_to_plot_s_s[j], positions=[x_positions[j] + 0.2], widths=0.3, patch_artist=True, boxprops=dict(facecolor=lighter_color))
            
            # Collect boxplot elements for legend
            if j == 0:  # Only need to add the first boxplot to the legend
                boxplot_elements.append(bp_normal["boxes"][0])
                boxplot_elements.append(bp_s_s["boxes"][0])

        # Set the x-axis labels mapping the integer positions to the corresponding time steps
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_values)
        ax.set_xlabel('Time steps (minutes)', fontsize=10)  # Reduced font size
        ax.set_ylabel(f'{category} Cells', fontsize=10)  # Reduced font size
        # Adjust the font size for the axis tick labels
        ax.tick_params(axis='x', labelsize=8)  # Reduced font size
        ax.tick_params(axis='y', labelsize=8)  # Reduced font size
        # Set the title for each subplot
        ax.set_title(f'{letters[i]}) {category} Cells', fontsize=10)  # Reduced font size

        # Set the legend location based on the category
        if category == 'mesenchymal':
            loc = 'lower right'
        else:
            loc = 'upper right'
        ax.legend(boxplot_elements, ['Continuous', 'Start-Stop'], loc=loc, fontsize=8)  # Reduced font size

    # Adjust the layout to make room for the main title
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # Save the figure to the specified output directory
    plt.savefig(os.path.join(output_dir, 'combined_cells_boxplot_second.pdf'))
    # Close the figure to free up memory
    plt.close()
    
def quantitative_test(output_dir):
    dir = os.getcwd()

    num_simu = 50

    step = 600

    two_D = True


    epithelial_s_s, mesenchymal_s_s, durations_ss = test_start_and_stop_second(num_simu, step, two_D)

    os.chdir(dir)

    epithelial, mesenchymal, durations = test_single_simu_second(num_simu, step, two_D)

    data = {
        'epithelial': epithelial,
        'mesenchymal': mesenchymal,
        'Durations': durations,
        'epithelial_Start_Stop': epithelial_s_s,
        'mesenchymal_Start_Stop': mesenchymal_s_s,
        'Durations_Start_Stop': durations_ss
    }
    
    data = convert_int64(data)
    # save the data as json
    with open(os.path.join(output_dir, 'quantitative_test_second.json'), 'w') as f:
        json.dump(data, f, indent = 4)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run qualitative test with specified output directory.')
    parser.add_argument('output_dir', type=str, help='The output directory')

    args = parser.parse_args()

    quantitative_test(args.output_dir)

    create_combined_boxplots(args.output_dir)
