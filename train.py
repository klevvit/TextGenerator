# coding: utf-8

"""train.py: create a model using word pairs from given texts"""

import os
import sys
from collections import defaultdict
import argparse
import json
import re

__author__ = 'Lev Kovalenko'
__copyright__ = "Copyright 2018, Lev Kovalenko"
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '0.1.6'

# TODO: remove
import time
def time_measure(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__ + ':', time.clock() - t)
        return res
    return wrapper


def create_parser():
    """Create parser with argparse lib"""
    p = argparse.ArgumentParser(
        description='Create model for generator.',
        epilog='March 2018, Lev Kovalenko', add_help=True)
    p.add_argument('--input-dir', '-i',
                   help='optional; path to directory with text files (and '
                        'with NO directories!!!), read from standard input '
                        'stream if not stated')
    p.add_argument('--model', '-m', type=argparse.FileType('w'),
                   help='path to file for saving model')
    p.add_argument('--lc', '-l', action='store_true',
                   help='optional; convert words to lowercase')
    p.add_argument('--no-cleanup', '-nc', action='store_true',
                   help='optional; do not remove non-alphabetic symbols')
    p.add_argument('--min-quantity', '-mq', type=int,
                   help='optional; minimal quantity of word pairs in text '
                        'for saving them to model')
    return p


WORD_SEPARATOR = ' '  # Const

model = defaultdict(lambda: defaultdict(int))
# Key: first_word, Val: {Key: second_word, Val: quantity1}


def process_string(dirty_string, lower, cleanup):
    """Format sting as required before the next step.

    Replace whitespace symbols with spaces. Optionally convert symbols to
    lowercase and/or remove all symbols except letters, digits and spaces.
    :param dirty_string: the string to be processed
    :param lower: True if must convert to lowercase, False otherwise
    :param cleanup: True if must remove non-alphabetic symbols, False
    otherwise.
    :return: the result of processing
    """
    clean_string = re.sub(r'\s+', ' ', dirty_string)  # replace whitespace
    if cleanup:
        clean_string = re.sub(r'[^ \w]', '', dirty_string)
    if lower:
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


def read_stream(stream, lower, cleanup):
    """Add word pairs from the input stream into model

    Read all the text from stream, process it if necessary, split into words,
    add every word pair into model. Do not close stream!

    :param stream: input stream
    :param lower: True if must convert to lowercase, False otherwise
    :param cleanup: True if must remove non-alphabetic symbols, False
    otherwise.
    """
    words = []
    for line in stream:
        words += process_string(line, lower, cleanup).split()
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


@time_measure
def train():
    # Read parameters
    parser = create_parser()
    args = parser.parse_args()
    input_dir = args.input_dir

    if input_dir is None:
        read_stream(sys.stdin, args.lc, not args.no_cleanup)
    else:
        file_list = get_all_files(input_dir)
        for file_path in file_list:
            f = open(file_path, 'r')
            read_stream(f, args.lc, not args.no_cleanup)
            f.close()
    # Output
    f = args.model
    write_model(f, args.min_quantity)
    f.close()


if __name__ == '__main__':
    train()
