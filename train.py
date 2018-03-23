import os
import sys
from collections import defaultdict
import argparse


def create_parser():
    """Create parser

    Create parser with arguments:
    --input-dir, -i     optional; path to directory with text files and with
                        NO directories; read from standard input stream if
                        not stated
    --model, -m         path to file for saving model
    --lc, -l            optional; convert words to lowercase
    --help, -h          default argparse help
    :return: generated parser
    """
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


def read_stream(stream, lc):
    """Add word pairs from the input stream into dictionary

    Read all the text from stream, process it if necessary, split into words,
    add every word pair into dictionary. Do not close stream!

    :param stream: input stream
    :param lc: True if must convert to lowercase, False otherwise.
    """
    is_end_of_stream = False
    line = stream.readline()
    while not is_end_of_stream:
        line = clean_up(line)
        if lc:
            line = line.lower()
        line = line.split()
        for i in range(0, len(line) - 1):
            add_to_dict(line[i], line[i + 1])
        new_line = stream.readline()
        if new_line == '':
            is_end_of_stream = True
        line = line[-1] + ' ' + new_line


# Read parameters
parser = create_parser()
args = parser.parse_args()
input_dir = args.input_dir

if input_dir is None:
    read_stream(sys.stdin, args.lc)
else:
    if input_dir[-1] != '/':
        input_dir += '/'
    listdir = os.listdir(input_dir)
    for filename in listdir:
        if filename[0] == '.':
            continue
        f = open(input_dir + filename, 'r')
        read_stream(f, args.lc)
        f.close()

# Output
f = args.model
for tup in d.items():
    f.write('{words} {num}\n'.format(words=tup[0], num=tup[1]))
f.close()
