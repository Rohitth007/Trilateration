import argparse
from ast import literal_eval as ast_eval
import os
import random

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from trilateration import euclidean_dist


DELIM = ' | '

location_files = [
    '_noisy_locs_2.csv',
    '_noisy_locs_1.csv',
    '_noisy_locs_05.csv',
    '_pure_locs.csv',
]


def main(file_id, show_before_after):
    for in_file in location_files:
        error_per_anchor = []
        in_file = file_id + in_file
        print(f'\n Parsing file {in_file} and true_locations.csv pairwise...')

        with open('true_locations.csv') as truth, open(in_file) as measured:
            # Parsing 100 anchor case pairs.
            for truth_anchor_case, measured_anchor_case in zip(truth, measured):
                trilat_errors = []
                anchor_triplet = ast_eval(truth_anchor_case.split(DELIM)[0])
                true_nodes = truth_anchor_case.split(DELIM)[1:]
                measured_nodes = measured_anchor_case.split(DELIM)[1:]

                # Parsing 50 node case pairs for each anchor case.
                for true_node, measured_node in zip(true_nodes, measured_nodes):
                    true_node = ast_eval(true_node)
                    measured_node = ast_eval(measured_node)
                    error = euclidean_dist(true_node, measured_node)
                    trilat_errors.append(error)
                    if show_before_after:
                        plt.scatter(
                            true_node[0], true_node[1], color='r', alpha=0.5)
                        plt.scatter(
                            measured_node[0], measured_node[1], color='b', alpha=0.5)

                if show_before_after:
                    for anchor in anchor_triplet:
                        plt.scatter(
                            anchor[0], anchor[1], color='y', s=10**3, alpha=0.2)
                    plt.subplots_adjust(left=0.20, right=0.79)
                    plt.title('Larger circles marks anchor points')
                    plt.legend(['before', 'after'])
                    plt.show()

                error_per_anchor.append(np.median(trilat_errors))

            plt.bar(range(1, 101), error_per_anchor, alpha=0.7, width=0.8)
            plt.xlim(0, 101)

    plt.xlabel('Anchor Triplet Number')
    plt.ylabel('Median Error')
    plt.legend(['Error 2', 'Error 1', 'Error 0.5', 'Pure'])
    plt.subplots_adjust(left=0.03, right=0.99, top=0.96, bottom=0.11)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_id", help="brute-step used for trilateration", default='')
    parser.add_argument("--show_before_after", action='store_true')

    args = parser.parse_args()
    file_id = args.file_id
    show_before_after = args.show_before_after

    print(f'\n Using files with starting with "{file_id}_"')

    print('\n Localization Errors per Anchor Triplet')
    try:
        # Setting Matplotlib settings
        plt.style.use('seaborn-darkgrid')
        if not show_before_after:
            plt.figure(figsize=(20, 4))
        else:
            print('\n Showing groundtruth vs after trilaterization.\
                   \n Use Ctrl+C to exit')
            random.shuffle(location_files)

        main(file_id, show_before_after)

    except FileNotFoundError:
        print('\nError: Make sure you have run "generate_dataset.py" and \
               \n       "trilatertion.py" with corresponding brute_step\n')
