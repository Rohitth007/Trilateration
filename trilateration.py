import argparse
from ast import literal_eval as ast_eval
import os

import numpy as np
from math import sqrt
from lmfit import minimize, Parameters


DELIM = ' | '

range_files = [
    'pure_ranges.csv',
    'noisy_ranges_05.csv',
    'noisy_ranges_1.csv',
    'noisy_ranges_2.csv'
]


def main(brute_step):
    for in_file in range_files:
        nodes = np.zeros((100, 50, 2))
        out_file = f'{brute_step}_' + in_file.replace('range', 'loc')

        print(f'\nParsing file {in_file}...')
        with open(in_file, 'r') as f:
            for i, line in enumerate(f):
                ranges = line.split(DELIM)
                anchor_triplet = ast_eval(ranges[0])
                measured_ranges = map(ast_eval, ranges[1:])

                print(
                    f'Trilaterating 50 nodes of anchor case {i+1}...',
                    end='\r'
                )

                # Trilaterate each node-case for an anchor-case
                nodes_per_anchor_case = []
                for range_triplet in measured_ranges:
                    node = trilaterate(
                        anchor_triplet, range_triplet, brute_step
                    )
                    node = tuple(map(round, node))
                    nodes_per_anchor_case.append(node)

                # Write trilaterated nodes to outfile.
                with open(out_file, 'a') as f:
                    f.write(str(anchor_triplet) + DELIM)
                    f.write(DELIM.join(map(str, nodes_per_anchor_case)) + '\n')

        print(f'\nWriting output to file {out_file}.')


def trilaterate(anchor_triplet, range_triplet, brute_step):

    def residual(node, anchors, data):
        model = np.empty(len(anchors))
        eps_data = [0.1, 0.1, 0.1]
        node = (node['x'], node['y'])

        for i, anchor in enumerate(anchors):
            model[i] = euclidean_dist(anchor, node)

        return (data - model) / eps_data

    # Bruteforcing for finding best starting point.
    if brute_step:
        init = Parameters()
        init.add('x', min=0, max=99, brute_step=brute_step)
        init.add('y', min=0, max=99, brute_step=brute_step)

        init_soln = minimize(
            residual, init,
            args=(anchor_triplet, range_triplet),
            method='brute'
        )
    else:
        init_x = 50
        init_y = 50

    node = Parameters()
    init_x = init_soln.params['x'].value
    init_y = init_soln.params['y'].value
    node.add('x', value=init_x, min=0, max=99)
    node.add('y', value=init_y, min=0, max=99)

    node_soln = minimize(residual, node, args=(anchor_triplet, range_triplet))

    return node_soln.params['x'].value, node_soln.params['y'].value


def euclidean_dist(point1: tuple, point2: tuple):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--brute_step", help="brute-step used for trilateration", type=int)

    brute_step = parser.parse_args().brute_step

    if brute_step:
        print('\n Least Square Trilateration using brute_step', brute_step)
        re = f'{brute_step}_'
    else:
        print('\n Least Square Trilateration using starting point (50,50)')
        brute_step = ''
        re = '[^\d]'

    # Delete old files as same files would be appended.
    input('\n This would delete corresponding old trilateration .csv files. \
           \n Make sure to backup if wanting to preserve them. \
           \n Make sure correct --brute_step is/is not applied. \
           \n Press Any key to continue, Ctrl-C to exit.')

    print('\n Removing old trilateration .csv files if present...')
    os.system(f'ls | grep -P "^{re}.+_locs.*\.csv" | xargs rm -v 2>/dev/null')

    print('\nTrilaterating 50 nodes for each of the 100 anchor cases...')
    try:
        main(brute_step)
    except FileNotFoundError:
        print('\nError: Make sure you have run generate_dataset.py\n')
