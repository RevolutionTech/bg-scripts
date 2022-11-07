from collections import Counter, defaultdict
from typing import List
import csv
import os

from nltk.corpus import words

SCRATCH_DIR = "scratch"
WORD_LENGTH_MIN = 4
WORD_LENGTH_MAX = 6
NGRAM_LENGTH_MIN = 2
NGRAM_LETTER_EMPTY = "█"
NGRAM_LETTER_SEPARATOR = " "
NGRAM_FREQUENCY_MIN = 30

def generate_ngrams_for_word(word: str) -> List[str]:
    ngrams = []

    word_len = len(word)
    for ngram_start_pos in range(word_len + 1 - NGRAM_LENGTH_MIN):
        for ngram_length in range(NGRAM_LENGTH_MIN, min(word_len + 1 - ngram_start_pos, word_len - 1)):
            ngram_letters = []
            for ngram_letter_pos, letter in enumerate(word):
                if ngram_letter_pos < ngram_start_pos or ngram_letter_pos >= ngram_start_pos + ngram_length:
                    ngram_letters.append(NGRAM_LETTER_EMPTY)
                else:
                    ngram_letters.append(letter)
            ngram = NGRAM_LETTER_SEPARATOR.join(ngram_letters).upper()
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
            csvwriter = csv.writer(f)
            csvwriter.writerow(["Ngram", "Frequency"])

            ngram_counter = positional_ngrams[word_len]
            for ngram, frequency in ngram_counter.most_common():
                if frequency < NGRAM_FREQUENCY_MIN:
                    # We don't care about incredibly rare ngrams
                    break
                csvwriter.writerow((ngram, frequency))

        word_count = word_len_frequency[word_len]
        print("Total words:", word_count)

if __name__ == "__main__":
    runscript()
