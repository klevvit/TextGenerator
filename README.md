# TextGenerator

A word sequence generator. The main executable files are [train.py](train.py) and [generate.py](generate.py).

### From `train.py --help`:

```
usage: train.py [-h] [--input-dir INPUT_DIR] [--model MODEL] [--lc]
                [--no-cleanup] [--min-quantity MIN_QUANTITY]

This program reads given text files, then creates a model file that contains
all pairs of words from the texts with quantities of their occurrences. The
model file can be used later in generate.py to create a sequence of words
where all adjacent words are related in sense (read more in generate.py help).

options:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR, -i INPUT_DIR
                        optional; path to directory with TEXT FILES ONLY, it
                        may contain subdirectories with text files; read from
                        standard input stream if not stated
  --model MODEL, -m MODEL
                        path to file for saving model; if file exists, it will
                        be overwritten
  --lc, -l              optional; convert words to lowercase
  --no-cleanup, -nc     optional; do not remove non-alphabetical symbols
  --min-quantity MIN_QUANTITY, -mq MIN_QUANTITY
                        optional; minimal quantity of word pairs in all texts
                        for saving them to the model
```

### From `generate.py --help`:

```
usage: generate.py [-h] [--model MODEL] [--seed SEED] [--length LENGTH]
                   [--output OUTPUT]

This program reads given model file (you can generate it with train.py) and
creates a sequence of words. If the seed was not stated, the first word is a
random one from the texts; all words have equal chances to be the first, no
matter how often they have appeared in the texts. Every next word is one of
the words that go after the previous one in texts; and here the quantity of
appearances after that word is taken into account. If the previous word has no
pairs, the next one wil be selected randomly, like if it would be the first
one.

options:
  -h, --help            show this help message and exit
  --model MODEL, -m MODEL
                        path to the model file; use train.py to generate a
                        model
  --seed SEED, -s SEED  optional; the first word in sequence, must be the word
                        that exists at least in one of the texts, with
                        required format if it was set for generation of the
                        model (lowercase, with non-alphabetical symbols,
                        etc.); random word from all the texts if not stated.
  --length LENGTH, -l LENGTH
                        length of the sequence that will be generated
  --output OUTPUT, -o OUTPUT
                        optional; path to the output file; if file exists, it
                        will be overwritten; write to standard output stream
                        if not stated
```
