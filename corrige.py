import argparse
import sys
from sys import stdin

import distances


def read_glossary(glossary_file):
    glossary = {}
    with open(glossary_file, 'r') as glossary_file:
        lines = glossary_file.read().split('\n')
        lines.remove('')
        for line in lines:
            f, w = line.strip().split(' ')
            glossary[w] = int(f)
    return glossary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('glossary', type=str, help='Glossary file where to find right words.')
    args, _ = parser.parse_known_args(sys.argv[1:])

    glossary = read_glossary(args.glossary)

    words = stdin.read().split('\n')
    words.remove('')

    distance = distances.JaccardDistance(glossary=glossary, max_proposition=5, selection_method_id=2, nb_char=2)
    all_props = distance.propositions(words)

    for word, props in all_props.items():
        print(word, '\t'.join(props), sep='\t')



