from collections import defaultdict
import random


# def weighted_choice(choices):
#     total = sum(w for c, w in choices)
#     r = random.uniform(0, total)
#     upto = 0
#     for c, w in choices:
#         if upto + w >= r:
#             return c
#         upto += w
#     assert False, "Shouldn't get here"


WORD_SEPARATOR = ' '  # Const
d_pair = defaultdict(list)
d_quantity = defaultdict(int)
with open('dict.txt', 'r') as f:
    line = f.readline()
    while line != '':
        tup = line.split(WORD_SEPARATOR)
        d_pair[tup[0]].append(tup[1])
        d_quantity[tup[0] + WORD_SEPARATOR + tup[1]] = int(tup[-1])
        line = f.readline()
words_to_output = 100
with open('output.txt', 'w') as f:
    word = 
    for i in range(words_to_output):

# debug output
print(d_pair)
