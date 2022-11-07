from collections import Counter, defaultdict
from typing import List

from nltk.corpus import words

WORD_LENGTH_MIN = 4
WORD_LENGTH_MAX = 6
NGRAM_LENGTH_MIN = 2
NGRAM_LETTER_EMPTY = "█"
NGRAM_LETTER_SEPARATOR = " "
NGRAM_MOST_COMMON_NUM = 10

def generate_ngrams_for_word(word: str) -> List[str]:
    ngrams = []

    word_len = len(word)
    for ngram_start_pos in range(word_len + 1 - NGRAM_LENGTH_MIN):
        for ngram_length in range(NGRAM_LENGTH_MIN, word_len + 1 - ngram_start_pos):
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
    positional_ngrams = defaultdict(Counter)

    for word in words.words():
        word_len = len(word)
        if WORD_LENGTH_MIN <= word_len <= WORD_LENGTH_MAX:
            ngrams = generate_ngrams_for_word(word)
            positional_ngrams[word_len].update(ngrams)

    return positional_ngrams

def runscript():
    positional_ngrams = generate_positional_ngrams()

    print("Most common ngrams:")
    for word_len in range(WORD_LENGTH_MIN, WORD_LENGTH_MAX + 1):
        ngram_count = positional_ngrams[word_len]
        print(f"{word_len}-Letter word:", ngram_count.most_common(NGRAM_MOST_COMMON_NUM))

if __name__ == "__main__":
    runscript()
