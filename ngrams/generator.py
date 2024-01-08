import itertools
from collections import Counter, defaultdict

from nltk.corpus import words

from ngrams.constants import (
    WORD_LENGTH_MIN,
    WORD_LENGTH_MAX,
    NGRAM_LENGTH_MIN,
    NGRAM_LETTER_EMPTY,
)


class NgramGenerator:
    def __init__(self):
        self._letter_frequency = Counter()
        self._word_len_frequency = Counter()
        self._positional_ngrams = defaultdict(Counter)

    def generate_ngrams_for_word(self, word: str):
        word_len = len(word)
        for ngram_length in range(NGRAM_LENGTH_MIN, word_len + 1 - NGRAM_LENGTH_MIN):
            for blank_indices in itertools.combinations(range(word_len), ngram_length):
                ngram_letters = []
                for i, letter in enumerate(word):
                    uletter = letter.upper()
                    if i in blank_indices:
                        ngram_letters.append(NGRAM_LETTER_EMPTY)
                        self._letter_frequency[uletter] += 1
                    else:
                        ngram_letters.append(uletter)
                ngram = "".join(ngram_letters)
                self._positional_ngrams[word_len][ngram] += 1

    def get_letter_counts(self):
        return sorted(self._letter_frequency.items())

    def get_word_count(self, word_length):
        return self._word_len_frequency[word_length]

    def get_ngrams_with_frequencies(self, word_length):
        ngram_counter = self._positional_ngrams[word_length]
        return ngram_counter.most_common()

    def generate(self):
        for word in words.words():
            word_len = len(word)
            if WORD_LENGTH_MIN <= word_len <= WORD_LENGTH_MAX:
                self._word_len_frequency[word_len] += 1
                self.generate_ngrams_for_word(word)
