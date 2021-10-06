import argparse
import sys
from math import *
from sys import stdin

import numpy as np


def read_eval_file(eval_file):
    eval_data = {}
    with open(eval_file, 'r') as eval_file:
        lines = eval_file.read().split('\n')
        lines.remove('')
        for line in lines:
            w, p = line.split('\t')
            eval_data[w] = p
    return eval_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('eval_file', type=str, help='Evaluation file.')
    parser.add_argument('-p', '--power', default=2, type=int, help='Minkowski power.')
    args, _ = parser.parse_known_args(sys.argv[1:])

    eval_data = read_eval_file(args.eval_file)

    words = stdin.read().split('\n')
    words.remove('')

    scores = []

    for line in words:
        line = line.split('\t')
        word = line[0]
        props = line[1:]

        p0 = eval_data[word]
        nb_props = len(props)
        try:
            i_prop = props.index(p0)
        except ValueError:
            i_prop = nb_props

        score = sqrt(1 - (i_prop/nb_props)**args.power)
        scores.append(score)
    print(np.mean(scores))
