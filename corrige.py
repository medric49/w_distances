import argparse
import sys
from sys import stdin

import distances
from utils import read_glossary

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('glossary', type=str, help='Glossary file where to find right words.')
    args, _ = parser.parse_known_args(sys.argv[1:])

    glossary = read_glossary(args.glossary)

    words = stdin.read().split('\n')
    words.remove('')

    distance = distances.JaccardDistance(nb_char=2, glossary=glossary, max_proposition=5, select_fn=2)
    all_props = distance.propositions(words)

    for word, props in all_props.items():
        print(word, '\t'.join(props), sep='\t')



