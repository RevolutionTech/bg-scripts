from collections import Counter, defaultdict
from typing import List
import csv
import itertools
import os

from nltk.corpus import words

SCRATCH_DIR = "scratch"
WORD_LENGTH_MIN = 4
WORD_LENGTH_MAX = 6
NGRAM_LENGTH_MIN = 2
NGRAM_LETTER_EMPTY = "█"
NGRAM_FREQUENCY_MIN = 30

def make_ordinal(n: int) -> str:
    """
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'

    Source: https://stackoverflow.com/a/50992575/3241924
    """
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix

def generate_ngrams_for_word(word: str) -> List[str]:
    ngrams = []

    word_len = len(word)
    for ngram_length in range(NGRAM_LENGTH_MIN, word_len + 1 - NGRAM_LENGTH_MIN):
        for blank_indices in itertools.combinations(range(word_len), ngram_length):
            ngram_letters = []
            for i, letter in enumerate(word):
                if i in blank_indices:
                    ngram_letters.append(NGRAM_LETTER_EMPTY)
                else:
                    ngram_letters.append(letter)
            ngram = "".join(ngram_letters).upper()
            ngrams.append(ngram)

    return ngrams

def generate_positional_ngrams():
    word_len_frequency = Counter()
    positional_ngrams = defaultdict(Counter)

    for word in words.words():
        word_len = len(word)
        if WORD_LENGTH_MIN <= word_len <= WORD_LENGTH_MAX:
            word_len_frequency[word_len] += 1
            ngrams = generate_ngrams_for_word(word)
            positional_ngrams[word_len].update(ngrams)

    return word_len_frequency, positional_ngrams

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
                letter_cells = [letter.replace(NGRAM_LETTER_EMPTY, "") for letter in ngram]
                csvwriter.writerow([*letter_cells, frequency])

        word_count = word_len_frequency[word_len]
        print("Total words:", word_count)

if __name__ == "__main__":
    runscript()
