import os
from random import sample
from math import sqrt

import numpy as np
from trilateration import euclidean_dist


GRID_SIZE = 100
DELIM = ' | '


def main():
    # Simulate 100x100 grid
    grid = set()
    for rows in range(GRID_SIZE):
        for cols in range(GRID_SIZE):
            grid.add((rows, cols))

    used_anchors = []
    for anchor_case in range(100):
        # Sample 3 anchors from locs not already chosen. (unique)
        anchor_triplet = tuple(sample(grid - set(used_anchors), 3))
        used_anchors.extend(anchor_triplet)

        # 50 unique node cases for each anchor case
        node_locs_per_triplet = sample(grid - set(anchor_triplet), 50)

        with open('true_locations.csv', 'a') as f:
            f.write(str(anchor_triplet) + DELIM)
            f.write(DELIM.join(map(str, node_locs_per_triplet)) + '\n')

        # Finds range triplet of node from anchor triplets
        pure_ranges_per_triplet = []
        for node in node_locs_per_triplet:
            range_triplet = []
            for anchor in anchor_triplet:
                _range = euclidean_dist(anchor, node)
                range_triplet.append(_range)
            pure_ranges_per_triplet.append(tuple(range_triplet))

        with open('pure_ranges.csv', 'a') as f:
            f.write(str(anchor_triplet) + DELIM)
            f.write(DELIM.join(map(str, pure_ranges_per_triplet)) + '\n')

        # Add Gaussian Noise to pure ranges
        def add_noise(mu, sigma=0.1):
            noise = np.random.normal(mu, sigma, (50, 3))
            noisy_ranges = pure_ranges_per_triplet + noise
            return tuple(map(tuple, noisy_ranges))

        for fnum, mean in {'05': 0.5, '1': 1, '2': 2}.items():
            with open(f'noisy_ranges_{fnum}.csv', 'a') as f:
                f.write(str(anchor_triplet) + DELIM)
                f.write(DELIM.join(map(str, add_noise(mean))) + '\n')


if __name__ == '__main__':
    # Delete old files as same files would be appended.
    input('\n This would delete the old range dataset .csv files. \
           \n Make sure to backup if wanting to preserve them. \
           \n Press Any key to continue, Ctrl-C to exit.')

    print('\nRemoving old dataset .csv files if present...')
    os.system('ls | grep -P "(?:_ranges|true_).*\.csv" | xargs rm -v 2>/dev/null')

    print('\nGenerating Trilateration Range Dataset...')
    main()

    print('\nCreated 50 node cases for each of the 100 anchor triplets.')
    print('* Nodes stored in true_locations.csv')
    print('* Ground-truth ranges stored in pure_ranges.csv')
    print('* Gaussian noisy ranges with:')
    print('  - mean 0.5 stored in noisy_ranges_05.csv')
    print('  - mean 1 stored in noisy_ranges_1.csv')
    print('  - mean 2 stored in noisy_ranges_2.csv')
