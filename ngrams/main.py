import csv
import os

from ngrams.constants import (
    SCRATCH_DIR,
    WORD_LENGTH_MIN,
    WORD_LENGTH_MAX,
    NGRAM_LETTER_EMPTY,
    NGRAM_FREQUENCY_MIN,
)
from ngrams.generator import generate_positional_ngrams
from ngrams.utils import make_ordinal


def runscript():
    word_len_frequency, positional_ngrams = generate_positional_ngrams()

    for word_len in range(WORD_LENGTH_MIN, WORD_LENGTH_MAX + 1):
        filename = os.path.join(SCRATCH_DIR, f"word-{word_len}.csv")
        print(f"Writing {filename}...")

        with open(filename, "w") as f:
            letter_headers = [f"{make_ordinal(i + 1)} Letter" for i in range(word_len)]
            headers = [*letter_headers, "Frequency"]
            csvwriter = csv.writer(f)
            csvwriter.writerow(headers)

            ngram_counter = positional_ngrams[word_len]
            for ngram, frequency in ngram_counter.most_common():
                if frequency < NGRAM_FREQUENCY_MIN:
                    # We don't care about incredibly rare ngrams
                    break
                letter_cells = [
                    letter.replace(NGRAM_LETTER_EMPTY, "") for letter in ngram
                ]
                csvwriter.writerow([*letter_cells, frequency])

        word_count = word_len_frequency[word_len]
        print("Total words:", word_count)


if __name__ == "__main__":
    runscript()
