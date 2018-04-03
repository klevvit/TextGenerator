# coding: utf-8

"""train.py: create a model using word pairs from given texts"""

import os
import sys
from collections import OrderedDict
import argparse

__author__ = 'Lev Kovalenko'
__copyright__ = "Copyright 2018, Lev Kovalenko"
__credits__ = ['Lev Kovalenko', 'Kseniya Kolesnikova']

__version__ = '0.1.2'


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


d = OrderedDict(int)    # Dict [word pair | quantity]
WORD_SEPARATOR = ' '    # Const


def process_string(dirty_string, lower, cleanup):
    """Format sting as required before the next step.

    Replace whitespace symbols with spaces. Optionally convert symbols to
    lowercase and/or remove all the symbols except letters and spaces.
    :param dirty_string: the string to be processed
    :param lower: True if must convert to lowercase, False otherwise
    :param cleanup: True if must remove non-alphabetic symbols, False
    otherwise.
    :return: the result of processing
    """
    clean_string = ''
    for char in dirty_string:
        if char.isspace():
            clean_string += ' '
        elif not cleanup or char.isalpha():
            clean_string += char
    if lower:
        clean_string = clean_string.lower()
    return clean_string


def add_to_dict(word1, word2):
    """Add the word pair to the dictionary

    Merge two words into one string separated by WORD_SEPARATOR.
    In dictionary d, increment value by 1 for this string key if
    exists, create such key with value 1 otherwise.
    :param word1: the first word in pair
    :param word2: the second word in pair
    """
    global d
    string_pair = word1 + ' ' + word2
    d[string_pair] += 1


def read_stream(stream, lower, cleanup):
    """Add word pairs from the input stream into dictionary

    Read all the text from stream, process it if necessary, split into words,
    add every word pair into dictionary. Do not close stream!

    :param stream: input stream
    :param lower: True if must convert to lowercase, False otherwise
    :param cleanup: True if must remove non-alphabetic symbols, False
    otherwise.
    """
    is_end_of_stream = False
    line = stream.readline()
    while not is_end_of_stream:
        line = process_string(line, lower, cleanup)
        line = line.split()
        for i in range(0, len(line) - 1):
            add_to_dict(line[i], line[i + 1])
        new_line = stream.readline()
        if new_line == '':
            is_end_of_stream = True
        if not line:
            line = new_line
        else:
            line = line[-1] + ' ' + new_line


def get_all_files(directory):
    """Return list of paths to all files in directory and all subdirectories"""
    list_files = []
    for di, dirs, files in os.walk(directory):
        for file in files:
            if file[0] != '.':
                list_files.append(str(os.path.join(di, file)))
    return list_files


if __name__ == '__main__':
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
    if args.min_quantity is None:
        check = False
    else:
        check = True
    for tup in d.items():
        if not check or tup[1] > args.min_quantity:
            f.write('{words} {num}\n'.format(words=tup[0], num=tup[1]))
    f.close()
