import csv
import os

from nltk.corpus import words as nltk_words

from ngrams.constants import SCRATCH_DIR

NGRAMS_TXT = os.path.join(SCRATCH_DIR, "ngrams.txt")


def read_ngram_dictionary():
    nltk_dictionary = set(nltk_words.words())
    ngram_dictionary = set()

    with open(NGRAMS_TXT) as f:
        csvreader = csv.reader(f)
        for row, in csvreader:
            ngram_dictionary.add(row)

    return ngram_dictionary & nltk_dictionary
