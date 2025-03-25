import csv
import os

from polysemy.constants import SCRATCH_DIR


def read_concrete_words():
    words = []

    filename = os.path.join(SCRATCH_DIR, "concrete-words.csv")
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        next(csvreader)  # skip header
        for (word,) in csvreader:
            words.append(word)

    return words
