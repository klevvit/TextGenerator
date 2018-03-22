from collections import defaultdict
import random


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


WORD_SEPARATOR = ' '  # Const
d = defaultdict(list)  # Key: first_word,
# Val = [[second_word0, quantity0], [second_word1, quantity1], ...]
with open('dict.txt', 'r') as f:
    line = f.readline()
    while line != '':
        tup = line.split(WORD_SEPARATOR)
        d[tup[0]].append([tup[1], int(tup[-1])])
        line = f.readline()
output_times = 100
with open('output.txt', 'w') as f:
    word = None
    for i in range(output_times):
        next_words = d.get(word)
        if next_words is None:
            word = random.choice(list(d.keys()))
        else:
            word = weighted_choice(next_words)
        f.write(word + ' ')
