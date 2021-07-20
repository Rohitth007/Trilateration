from ast import literal_eval as ast_eval
from linecache import getline

from math import sqrt
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from trilateration import euclidean_dist


GRID_SIZE = 100
DELIM = ' | '


def main():
    range_triplets = {}

    # Select random anchor triplet and node
    anchor_case = randint(1, 100)
    node_case = randint(1, 50)

    print('Reading Dataset...')

    # Fetch Anchor and Node locations
    true_locs = getline('true_locations.csv', anchor_case).split(DELIM)
    anchor_triplet = ast_eval(true_locs[0])
    print('Anchor locations:', anchor_triplet)
    node_loc = ast_eval(true_locs[node_case])
    print('Node location:', node_loc)

    # Fetch pure range triplet
    pure_ranges = getline('pure_ranges.csv', anchor_case).split(DELIM)
    range_triplets['pure_ranges'] = ast_eval(pure_ranges[node_case])

    # Fetch noisy range triplets
    for file in ['noisy_ranges_05', 'noisy_ranges_1', 'noisy_ranges_2']:
        noisy_ranges = getline(f'{file}.csv', anchor_case).split(DELIM)
        range_triplets[file] = ast_eval(noisy_ranges[node_case])

    # RMS error of any grid location x,y ranges to measured ranges
    # Measures closeness to actual node.
    def rms_cost(x, y, range_triplet):
        square_error_sum = 0
        for anchor, measured_range in zip(anchor_triplet, range_triplet):
            calc_range = euclidean_dist(anchor, (x, y))
            error = calc_range - measured_range
            square_error_sum += error**2
        rms_error = sqrt(square_error_sum / 3)
        return rms_error

    for descr, range_triplet in range_triplets.items():
        max_cost = 0
        cost_map = np.zeros((GRID_SIZE, GRID_SIZE))
        # Measure the cost function at each cell on grid.
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cost = rms_cost(i, j, range_triplet)
                cost_map[j][i] = cost
                # Find max for normalizing
                if cost > max_cost:
                    max_cost = cost

        # Normalize data
        cost_map = cost_map / max_cost

        print(f'Plotting heatmap for {descr}...')
        plt.style.use('seaborn-talk')
        plt.title(descr)
        plt.imshow(cost_map, cmap='RdPu', interpolation=None)
        plt.ylim(-5, 104)
        plt.xlim(-5, 104)
        plt.colorbar()

        node_x, node_y = node_loc
        plt.scatter(node_x, node_y, c='black', marker='x')

        for anchor in anchor_triplet:
            anchor_x, anchor_y = anchor
            plt.scatter(anchor_x, anchor_y, c='olive')
        plt.legend(['Node', 'Anchor'])
        plt.show()


if __name__ == '__main__':
    try:
        main()
    except SyntaxError:
        print('\nError: Make sure you have run generate_dataset.py\n')
