import argparse
from ast import literal_eval as ast_eval
import os

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from trilateration import euclidean_dist


DELIM = ' | '

location_files = [
    '_pure_locs.csv',
    '_noisy_locs_05.csv',
    '_noisy_locs_1.csv',
    '_noisy_locs_2.csv'
]


def main(file_id):
    # Matplotlib Settings
    plt.figure(figsize=(20, 4))
    plt.style.use('seaborn-darkgrid')

    violin_data = []

    for in_file in location_files:
        trilat_errors = []
        in_file = file_id + in_file
        print(f'\n Parsing file {in_file} and true_locations.csv pairwise...')

        with open('true_locations.csv') as truth, open(in_file) as measured:
            # Parsing 100 anchor case pairs.
            for truth_anchor_case, measured_anchor_case in zip(truth, measured):
                true_nodes = truth_anchor_case.split(DELIM)[1:]
                measured_nodes = measured_anchor_case.split(DELIM)[1:]
                # Parsing 50 node case pairs for each anchor case.
                for true_node, measured_node in zip(true_nodes, measured_nodes):
                    true_node = ast_eval(true_node)
                    measured_node = ast_eval(measured_node)
                    error = euclidean_dist(true_node, measured_node)
                    trilat_errors.append(error)

            violin_data.append(trilat_errors)

        print(' Trilat Count:', len(trilat_errors))
        print(' Max Error:', max(trilat_errors))
        print(' Median Error:', np.median(trilat_errors))
        print(' 75th Percentile Error:', np.percentile(trilat_errors, 75))
        print(' 95th Percentile Error:', np.percentile(trilat_errors, 95))

        # Calculate PDF and CDF
        error_counts, error_bins = np.histogram(trilat_errors, bins=range(100))
        pdf = error_counts / len(trilat_errors)
        cdf = np.cumsum(pdf)

        print('\n Plotting CDF of corresponding trilateration errors...')
        plt.plot(error_bins[:-1], cdf, label=f"CDF:{in_file}", alpha=0.8)
        plt.fill_between(error_bins[:-1], pdf, alpha=0.2)
        plt.xlim(-1, 100)

    # Plot 1
    plt.title('CDF:Line, PDF:Shaded')
    plt.subplots_adjust(left=0.03, right=0.99, top=0.93, bottom=0.11)
    plt.xlabel('Error')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()

    print('\n Plotting Violin Plot for each range error.')

    # Plot 2
    plt.figure(figsize=(6, 10))
    plt.title('Normal')
    vplot = plt.violinplot(violin_data, showmedians=True, widths=0.75)
    for violin, color in zip(vplot['bodies'], ['goldenrod', 'c', 'coral', 'mediumvioletred']):
        violin.set_facecolor(color)
        violin.set_alpha(0.6)
    plt.ylabel('Error')
    plt.ylim(ymin=-1)
    plt.legend(['Pure', 'Error 0.5', 'Error 1', 'Error 2'])
    plt.subplots_adjust(top=0.96, bottom=0.03)
    plt.show()

    # Plot 3
    plt.title('Zoomed')
    vplot = plt.violinplot(violin_data, showmedians=True, widths=0.75)
    for violin, color in zip(vplot['bodies'], ['goldenrod', 'c', 'coral', 'mediumvioletred']):
        violin.set_facecolor(color)
        violin.set_alpha(0.6)
    plt.ylabel('Error')
    plt.ylim(0, 15)
    plt.legend(['Pure', 'Error 0.5', 'Error 1', 'Error 2'])
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_id", help="brute-step used for trilateration", default='')

    file_id = parser.parse_args().file_id
    print(f'\n Using files with starting with "{file_id}_"')

    print('\n Localization Errors per Range Measurement Error')
    try:
        main(file_id)
    except FileNotFoundError:
        print('\nError: Make sure you have run "generate_dataset.py" and \
               \n       "trilatertion.py" with corresponding brute_step\n')
