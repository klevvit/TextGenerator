from collections import defaultdict

WORD_SEPARATOR = ' '  # Const
d = defaultdict(int)
pairCounter = 0
with open('dict.txt', 'r') as f:
    line = f.readline()
    while line != '':
        tup = line.split(WORD_SEPARATOR)
        d[tup[0] + WORD_SEPARATOR + tup[1]] = int(tup[-1])
        pairCounter += int(tup[-1])
        new_line = f.readline()

# debug output
print(pairCounter)
print(d)
