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


class NgramGenerator:
    def __init__(self):
        self._word_len_frequency = Counter()
        self._positional_ngrams = defaultdict(Counter)

    @staticmethod
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

    def get_frequencies(self, word_length):
        return self._word_len_frequency[word_length]

    def get_ngrams_with_frequencies(self, word_length):
        ngram_counter = self._positional_ngrams[word_length]
        return ngram_counter.most_common()

    def generate(self):
        for word in words.words():
            word_len = len(word)
            if WORD_LENGTH_MIN <= word_len <= WORD_LENGTH_MAX:
                self._word_len_frequency[word_len] += 1
                ngrams = self.generate_ngrams_for_word(word)
                self._positional_ngrams[word_len].update(ngrams)
