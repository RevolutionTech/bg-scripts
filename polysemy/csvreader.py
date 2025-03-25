import csv
import os

from polysemy.constants import SCRATCH_DIR


def read_word_list(filename):
    words = []

    filename = os.path.join(SCRATCH_DIR, filename)
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        next(csvreader)  # skip header
        for word, *_ in csvreader:
            words.append(word)

    return words
