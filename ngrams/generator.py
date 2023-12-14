import itertools
from collections import Counter, defaultdict
from typing import List

from nltk.corpus import words

from ngrams.constants import (
    WORD_LENGTH_MIN,
    WORD_LENGTH_MAX,
    NGRAM_LENGTH_MIN,
    NGRAM_LETTER_EMPTY,
)


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
