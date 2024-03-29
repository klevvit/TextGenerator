# coding: utf-8
"""
========
train.py
========
Create a model using word pairs from given texts.
-------------------------------------------------
Reads given text files, then creates a model file that contains all pairs of
words from the texts with quantities of their occurrences. The model file can
be used later in generate.py to create a sequence of words where all adjacent
words are related in sense (read more in generate.py help).
"""

__author__ = 'Lev Kovalenko'
__copyright__ = "Copyright 2018, Lev Kovalenko"
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '1.1.1'

import os
import sys
from collections import defaultdict, Counter
import argparse
import json
import re

WORD_SEPARATOR = ' '  # Const


def create_parser():
    """Create parser with argparse lib"""
    parser = argparse.ArgumentParser(
        description='''This program reads given text files, then creates a
        model file that contains all pairs of words from the texts with
        quantities of their occurrences. The model file can be used later in
        generate.py to create a sequence of words where all adjacent words are
        related in sense (read more in generate.py help).''',
        epilog='May 2018, Lev Kovalenko', add_help=True)
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
                        help='optional; do not remove non-alphabetical '
                             'symbols')
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
        clean_string = re.sub(r'[^ \w]|\d', '', dirty_string)
    if params.lower:
        clean_string = clean_string.lower()
    return clean_string


def read_stream(stream, params):
    """Return processed word pairs from the input stream

    Read all the text from stream, process it if necessary, split into words,
    add every word pair into model, return it. Do not close stream!

    :param stream: input stream
    :param params: Params class with non-None values of lower and cleanup;
    lower: True if must convert to lowercase, False otherwise;
    cleanup: True if must remove non-alphabetical symbols, False
    otherwise.
    :return: Counter object that contains all word pairs from the text and
    their quantities; format: {(word1_str, word2_str): quantity_int}
    """
    processed_result = Counter()
    if params.lower is None or params.cleanup is None:
        raise TypeError('At least one of the variables in params is None')
    words = []
    for line in stream:
        words += process_string(line, params).split()
        if not words:
            continue
        processed_result.update(zip(words[:-1], words[1:]))
        words = [words[-1]]
    # save last word from stream; we don't want to lose it if it doesn't
    # appear in the text anywhere else
    if words:
        processed_result.update([(words[0], None)])
    return processed_result


def save_model(output_stream, model, min_quantity):
    """Remove rare pairs and write model to output_stream

    Remove pairs of words with quantity less than min_quantity, convert model
    to "dict of dicts" format  {word1: {word2: quantity}}  and write model to
    output_stream.
    """
    if min_quantity is not None and min_quantity > 1:
        model = Counter({pair: quantity for pair, quantity in model.items() if
                         quantity >= min_quantity})

    # Key: first_word, Val: {Key: second_word, Val: quantity1}
    converted_model = defaultdict(lambda: defaultdict(int))
    for (word1, word2), quantity in model.items():
        if word2 is not None:
            converted_model[word1][word2] = quantity
        else:
            # save last words from streams; we want to save each of them for
            # generate.py if it doesn't appear in the texts anywhere else
            converted_model[word1]

    json.dump(converted_model, output_stream, ensure_ascii=False,
              separators=(',', ':'))


def get_files_list(input_dir):
    """Return list of opened streams for all files in dir and all subdirs

    :param input_dir: **str** path to the directory with text files, it may
        contain subdirectories with text files, they will be opened too
    """
    return [open(str(os.path.join(directory, file)), 'r')
            for directory, subdirs, files in os.walk(input_dir)
            for file in files if file[0] != '.']


def train():
    # Read parameters
    args = create_parser().parse_args()
    input_dir = args.input_dir
    params = Params(args)

    model = Counter()  # [(word1, word2): quantity]
    stream_list = []
    try:
        if input_dir is None:
            stream_list = [sys.stdin]
        else:
            stream_list = get_files_list(input_dir)
        for stream in stream_list:
            model.update(read_stream(stream, params))
    finally:
        # we may want to print something to sys.stdout after (e.g., execution
        # time), so it mustn't be closed
        if input_dir is not None:
            for stream in stream_list:
                stream.close()
    # Output
    with args.model as file:
        save_model(file, model, args.min_quantity)


if __name__ == '__main__':
    train()
