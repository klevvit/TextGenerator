# coding: utf-8
"""
============
generate.py
============
generate a word sequence using model created by *train.py*
__________________________________________________________
Reads given model file (you can generate it with *train.py*) and creates a
sequence of words. If the seed was not stated, the first word is a random one
from the texts; all words have equal chances to be the first, no matter how
often they have appeared in the texts. Every next word is one of the words
that go after the previous in texts; and here the quantity of appearances
after that word is taken into account. If the previous word has no pairs, the
next one wil be selected randomly, like if it would be the first one."""

__author__ = 'Lev Kovalenko'
__copyright__ = 'Copyright 2018, Lev Kovalenko'
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '0.1.15'

import sys
import argparse
import random
import json
import train

WORD_SEPARATOR = train.WORD_SEPARATOR  # Const


def create_parser():
    """Create parser with argparse lib"""
    parser = argparse.ArgumentParser(
        description='''This program reads given model file (you can generate 
        it with train.py) and creates a sequence of words. If the seed was not 
        stated, the first word is a random one from the texts; all words have 
        equal chances to be the first, no matter how often they have appeared 
        in the texts. Every next word is one of the words that go after the 
        previous one in texts; and here the quantity of appearances after that 
        word is taken into account. If the previous word has no pairs, the 
        next one wil be selected randomly, like if it would be the first 
        one.''',
        epilog='April 2018, Lev Kovalenko', add_help=True)
    parser.add_argument('--model', '-m', type=argparse.FileType('r'),
                        help='path to the model file; use train.py '
                             'to generate a model')
    parser.add_argument('--seed', '-s',
                        help='optional; the first word in sequence, must be '
                        'the word that exists at least in one of the texts, '
                        'with required format if it was set for generation of '
                        'the model (lowercase, with non-alphabetical symbols, '
                        'etc.); random word from all the texts if not stated.')
    parser.add_argument('--length', '-l', type=int,
                        help='length of the sequence that will be generated')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'),
                        help='optional; path to the output file; if file '
                             'exists, it will be overwritten; write to '
                             'standard output stream if not stated')
    return parser


def weighted_choice(choices):
    """Select random element considering weights

    Select random element from the list where each element
    has its own probability of being selected
    :param choices: list of pairs [element, weight]
    :return: random element; None if list is empty
    """
    total = sum(weight for choice, weight in choices)
    rand = random.uniform(0, total)
    upto = 0
    for choice, weight in choices:
        if upto + weight >= rand:
            return choice
        upto += weight
    return None  # for an empty list


def deal_with_seed(seed, model):
    """Check seed in the model; throw exception if not exists

    Check if the seed word is in the keys of the model. raise KeyError if not.
    Do nothing if seed is None.
    :return: seed word
    """
    first_word = None
    if seed is not None:
        if model.get(seed) is None:
            raise KeyError('Seed not found in the model. Execute program '
                           'with --help flag to get information about '
                           'required format.')
        first_word = seed
    return first_word


def write_sequence(model, length, first_word=None, stream=sys.stdout):
    """Generate a sequence of words from model and write it to stream"""
    if stream is None:
        stream = sys.stdout
    word = None
    if first_word is not None:
        write_word(first_word, stream)
        length -= 1
        word = first_word

    for i in range(length):
        next_words = model.get(word)
        if not next_words:
            word = random.choice(list(model.keys()))
        else:
            word = weighted_choice(next_words.items())
        write_word(word, stream)


def write_word(word, stream=sys.stdout):
    """Write the word and space symbol to stream"""
    stream.write('{} '.format(word))


def generate():
    input_file = None
    output_stream = None
    try:
        args = create_parser().parse_args()
        input_file = args.model
        output_stream = args.output
        if output_stream is None:
            output_stream = sys.stdout
        # Key: first_word,  Val: {Key: second_word, Val: quantity1}
        model = json.load(input_file)

        first_word = deal_with_seed(args.seed, model)
        write_sequence(model, args.length, first_word, output_stream)
        output_stream.write('\n')

    finally:
        if input_file is not None:
            input_file.close()
        # we may want to print something to sys.stdout after (e.g., execution
        # time), so it mustn't be closed
        if output_stream is not None and output_stream != sys.stdout:
            output_stream.close()


if __name__ == '__main__':
    generate()
