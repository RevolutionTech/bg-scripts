import csv
import os
import string

from nltk.corpus import words as nltk_words

from ngrams.constants import SCRATCH_DIR

EOWL_DIR = os.path.join(SCRATCH_DIR, "eowl")


def read_ngram_dictionary():
    nltk_dictionary = set(nltk_words.words())
    eowl_dictionary = set()

    for letter in string.ascii_uppercase:
        with open(os.path.join(EOWL_DIR, f"{letter} Words.csv")) as f:
            csvreader = csv.reader(f)
            for row, in csvreader:
                eowl_dictionary.add(row)

    return eowl_dictionary & nltk_dictionary
