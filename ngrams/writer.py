import csv
import os

from ngrams.constants import (
    SCRATCH_DIR,
    WORD_LENGTH_MIN,
    WORD_LENGTH_MAX,
    NGRAM_LETTER_EMPTY,
    NGRAM_FREQUENCY_MIN,
)
from ngrams.generator import NgramGenerator
from ngrams.utils import make_ordinal


class NgramWriter:
    def __init__(self, ngrams: NgramGenerator):
        self.ngrams = ngrams

    def write_letter_counts(self):
        filename = os.path.join(SCRATCH_DIR, "letters.csv")
        print(f"Writing {filename}...")

        with open(filename, "w") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["Letter", "Frequency"])

            for letter, count in self.ngrams.get_letter_counts():
                csvwriter.writerow([letter, count])

    def write_ngrams(self, word_len: int):
        filename = os.path.join(SCRATCH_DIR, f"word-{word_len}.csv")
        print(f"Writing {filename}...")

        with open(filename, "w") as f:
            letter_headers = [f"{make_ordinal(i + 1)} Letter" for i in range(word_len)]
            headers = [*letter_headers, "Frequency"]
            csvwriter = csv.writer(f)
            csvwriter.writerow(headers)

            ngrams_with_frequencies = self.ngrams.get_ngrams_with_frequencies(word_len)
            for ngram, frequency in ngrams_with_frequencies:
                if frequency < NGRAM_FREQUENCY_MIN:
                    # We don't care about incredibly rare ngrams
                    break
                letter_cells = [
                    letter.replace(NGRAM_LETTER_EMPTY, "") for letter in ngram
                ]
                csvwriter.writerow([*letter_cells, frequency])

        word_count = self.ngrams.get_word_count(word_len)
        print("Total words:", word_count)

    def write_all_ngrams(self):
        for word_len in range(WORD_LENGTH_MIN, WORD_LENGTH_MAX + 1):
            self.write_ngrams(word_len)
