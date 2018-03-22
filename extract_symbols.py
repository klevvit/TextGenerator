
s = set()
i = 0
with open('book.txt', 'r') as f:
    c = f.readline()
    while c != '':
        s.update(set(c))
        c = f.readline()
        i += 1
print('Read OK')
with open('symbols_in_book.txt', 'w') as f:

    f.write(''.join(sorted(s)))
print('Write OK')
