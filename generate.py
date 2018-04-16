# coding: utf-8

"""generate.py: generate a word sequence using model created by train.py"""

import sys
import argparse
import random
import json

__author__ = 'Lev Kovalenko'
__copyright__ = 'Copyright 2018, Lev Kovalenko'
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '0.1.4'

WORD_SEPARATOR = ' '  # Const


def create_parser():
    """Create parser with argparse lib"""
    p = argparse.ArgumentParser(
        description='Generate funny sequence of words.',
        epilog='If the previous word has no pairs, the next word wil be '
               'selected randomly.\n'
               'April 2018, Lev Kovalenko', add_help=True)
    p.add_argument('--model', '-m', type=argparse.FileType('r'),
                   help='path to file with saved model')
    p.add_argument('--seed', '-s',
                   help='optional; the first word in sequence; random word '
                        'if not stated')
    p.add_argument('--length', '-l', type=int,
                   help='length of sequence that will be generated')
    p.add_argument('--output', '-o', type=argparse.FileType('w'),
                   help='optional; path to output file; write to standard '
                        'output stream if not stated')
    return p


def weighted_choice(choices):
    """Select random element considering weights

    Select random element from the list where each element
    has its own probability of being selected
    :param choices: list of pairs [element, weight]
    :return: random element
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    input_file = args.model

    d = json.load(input_file)
    # Key: first_word,  Val: {Key: second_word, Val: quantity1}
    input_file.close()

    length = args.length
    output_stream = args.output
    if output_stream is None:
        output_stream = sys.stdout
    word = None
    if args.seed is not None:
        word = args.seed
        if d.get(word) is None:
            raise KeyError('No such word in texts')
        output_stream.write(word + ' ')
        length -= 1

    for i in range(length):
        next_words = d.get(word)
        if not next_words:
            word = random.choice(list(d.keys()))
        else:
            word = weighted_choice(next_words.items())
        output_stream.write(word + ' ')
    output_stream.close()
