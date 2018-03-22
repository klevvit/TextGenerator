import os
from collections import defaultdict
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog='generator', description='creates dict.txt',
        epilog='March 2018, Lev Kovalenko')

    return parser


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


with open('book.txt', 'r') as f:
    isEndOfFile = False
    line = f.readline()
    while not isEndOfFile:
        line = clean_up(line)
        line = line.lower()
        line = line.split()
        for i in range(0, len(line) - 1):
            add_to_dict(line[i], line[i + 1])
        new_line = f.readline()
        if new_line == '':
            isEndOfFile = True
        line = line[-1] + ' ' + new_line
# Output
with open('dict.txt', 'w') as f:
    for tup in d.items():
        f.write('{words} {num}\n'.format(words=tup[0], num=tup[1]))
