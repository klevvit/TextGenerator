# coding: utf-8
"""train.py: create a model using word pairs from given texts.
Reads given text files, then creates a model file that contains all pairs of
words from the texts with quantities of their occurrences. The model file can
be used later in generate.py to create a sequence of words where all adjacent
words are related in sense (read more in generate.py help)."""

import os
import sys
from collections import defaultdict
import argparse
import json
import re
import time

__author__ = 'Lev Kovalenko'
__copyright__ = "Copyright 2018, Lev Kovalenko"
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '0.1.9'


# TODO: add param to functions
def time_measure(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__ + ':', time.clock() - t)
        return res
    return wrapper


WORD_SEPARATOR = ' '  # Const

model = defaultdict(lambda: defaultdict(int))
# Key: first_word, Val: {Key: second_word, Val: quantity1}


def create_parser():
    """Create parser with argparse lib"""
    parser = argparse.ArgumentParser(
        description='''This program reads given text files, then creates a 
        model file that contains all pairs of words from the texts with 
        quantities of their occurrences. The model file can be used later in 
        generate.py to create a sequence of words where all adjacent words are 
        related in sense (read more in generate.py help).''',
        epilog='April 2018, Lev Kovalenko', add_help=True)
    parser.add_argument('--input-dir', '-i',
                        help='optional; path to directory with TEXT FILES '
                             'ONLY, it may contain subdirectories with text '
                             'files; read from standard input stream if '
                             'not stated')
    parser.add_argument('--model', '-m', type=argparse.FileType('w'),
                        help='path to file for saving model; if file exists, '
                             'it will be overwritten')
    parser.add_argument('--lc', '-l', action='store_true',
                        help='optional; convert words to lowercase')
    parser.add_argument('--no-cleanup', '-nc', action='store_true',
                        help='optional; do not remove non-alphabetical symbols')
    parser.add_argument('--min-quantity', '-mq', type=int,
                        help='optional; minimal quantity of word pairs in all '
                        'texts for saving them to the model')
    return parser


class Params:
    """Parameters for word processing; made for convenient passing arguments"""
    lower = None
    cleanup = None

    def __init__(self, parser_args):
        self.lower = parser_args.lc
        self.cleanup = not parser_args.no_cleanup


def process_string(dirty_string, params):
    """Format sting as required before the next step.

    Replace whitespace symbols with spaces. Optionally convert symbols to
    lowercase and/or remove all symbols except letters, digits and spaces.
    :param dirty_string: the string to be processed
    :param params: Params class with values of lower and cleanup;
    lower: True if must convert to lowercase, False otherwise;
    cleanup: True if must remove non-alphabetical symbols, False
    otherwise
    :return: a processed string
    """
    clean_string = re.sub(r'\s+', ' ', dirty_string)  # replace whitespace
    if params.cleanup:
        clean_string = re.sub(r'[^ \w]', '', dirty_string)
    if params.lower:
        clean_string = clean_string.lower()
    return clean_string


def add_to_dict(word1, word2):
    """Add the word pair to the model

    In dictionary model, increment value of [word1][word2] by 1 for this string
    pair if exists, create with value 1 otherwise. If word2 is None, just add
    word1 into model with empty dictionary key if model[word1] doesn't exist.
    :param word1: the first word in pair
    :param word2: the second word in pair or None
    """
    global model
    if word2 is None:
        model[word1]  # just create first word if not exists
    else:
        model[word1][word2] += 1


def read_stream(stream, params):
    """Add word pairs from the input stream into model

    Read all the text from stream, process it if necessary, split into words,
    add every word pair into model. Do not close stream!

    :param stream: input stream
    :param params: Params class with non-None values of lower and cleanup;
    lower: True if must convert to lowercase, False otherwise;
    cleanup: True if must remove non-alphabetical symbols, False
    otherwise.
    """
    if params.lower is None or params.cleanup is None:
        raise TypeError('At least one of the variables in params is None')
    words = []
    for line in stream:
        words += process_string(line, params).split()
        for i in range(0, len(words) - 1):
            add_to_dict(words[i], words[i + 1])  # TODO make adding without for
                                                 # but how?
        words = [words[-1]]
    add_to_dict(words[0], None)  # add last word from stream if has no pairs


def write_model(output_stream, min_quantity):
    """Remove rare pairs and write model into output_stream

    Remove second words with quantity less than min_quantity and write model
    into output_stream.
    """

    if min_quantity is not None and min_quantity > 1:
        for word1, words2 in model.items():
            # write all we want to delete into list
            list_to_del = []
            for word, quantity in words2.items():
                if quantity < min_quantity:
                    list_to_del.append(word)
            for word in list_to_del:
                words2.pop(word)
    json.dump(model, output_stream, ensure_ascii=False, separators=(',', ':'))


def get_all_files(directory):
    """Return list of paths to all files in directory and all subdirectories"""
    list_files = []
    for di, dirs, files in os.walk(directory):
        for file in files:
            if file[0] != '.':
                list_files.append(str(os.path.join(di, file)))
    return list_files


def train():
    # Read parameters
    args = create_parser().parse_args()
    input_dir = args.input_dir
    params = Params(args)

    if input_dir is None:
        read_stream(sys.stdin, params)
    else:
        file_list = get_all_files(input_dir)
        for file_path in file_list:
            with open(file_path, 'r') as file:
                read_stream(file, params)
    # Output
    with args.model as file:
        write_model(file, args.min_quantity)


if __name__ == '__main__':
    train()
