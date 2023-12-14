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


def runscript():
    ngrams = NgramGenerator()
    ngrams.generate()

    for word_len in range(WORD_LENGTH_MIN, WORD_LENGTH_MAX + 1):
        filename = os.path.join(SCRATCH_DIR, f"word-{word_len}.csv")
        print(f"Writing {filename}...")

        with open(filename, "w") as f:
            letter_headers = [f"{make_ordinal(i + 1)} Letter" for i in range(word_len)]
            headers = [*letter_headers, "Frequency"]
            csvwriter = csv.writer(f)
            csvwriter.writerow(headers)

            ngrams_with_frequencies = ngrams.get_ngrams_with_frequencies(word_len)
            for ngram, frequency in ngrams_with_frequencies:
                if frequency < NGRAM_FREQUENCY_MIN:
                    # We don't care about incredibly rare ngrams
                    break
                letter_cells = [
                    letter.replace(NGRAM_LETTER_EMPTY, "") for letter in ngram
                ]
                csvwriter.writerow([*letter_cells, frequency])

        word_count = ngrams.get_frequencies(word_len)
        print("Total words:", word_count)


if __name__ == "__main__":
    runscript()
