import os
import sys
from collections import defaultdict
import argparse


def create_parser():
    """Create parser

    Create parser with arguments:
    --input-dir     optional; path to directory with text files; read from
                    standard input stream if not stated
    --model         path to file for saving model
    --lc            optional; convert words to lowercase
    --help          default argparse help
    """
    p = argparse.ArgumentParser(
        prog='Trainer', description='Create model for generator.',
        epilog='March 2018, Lev Kovalenko')
    p.add_argument('--input-dir', '-i', help='optional; path to directory with'
                                             'text files; read from standard'
                                             'input stream if not stated')
    p.add_argument('--model', '-m', help='path to file for saving model')
    p.add_argument('--lc', '-l', default=None, help='optional; convert words'
                                                    'to lowercase')
    # TODO deal with lowercase
    return p


d = defaultdict(int)
WORD_SEPARATOR = ' '  # Const


def clean_up(dirty_string):
    """Remove non-alphabetic symbols.

    Remove all the symbols except letters and spaces.
    :param dirty_string: the string to be processed
    :return: the result of processing
    """
    clean_string = ''
    for char in dirty_string:
        if char.isalpha():
            clean_string += char
        elif char.isspace():
            clean_string += ' '
    return clean_string


def add_to_dict(word1, word2):
    """Add the word pair to the dictionary

    Merge two words into one string separated by WORD_SEPARATOR.
    In dictionary d, increment value by 1 for this string key if
    exists, create such key with value 1 otherwise.
    :param word1: the first word in pair
    :param word2: the second word in pair
    """
    string_pair = word1 + ' ' + word2
    d[string_pair] += 1


parser = create_parser()
args = parser.parse_args()

f = None
if args.input_dir is None:
    f = sys.stdin
else:
    f = open('book.txt', 'r')  # TODO: make lists of files

modelPath = args.model

lowercase = True
if args.lc is None:
    lowercase = False


isEndOfFile = False
line = f.readline()
while not isEndOfFile:
    line = clean_up(line)
    if lowercase:
        line = line.lower()
    line = line.split()
    for i in range(0, len(line) - 1):
        add_to_dict(line[i], line[i + 1])
    new_line = f.readline()
    if new_line == '':
        isEndOfFile = True
    line = line[-1] + ' ' + new_line
f.close()
# Output
with open(modelPath, 'w') as f:
    for tup in d.items():
        f.write('{words} {num}\n'.format(words=tup[0], num=tup[1]))
