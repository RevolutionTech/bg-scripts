import os

TOP_DIR = os.path.dirname(os.path.dirname(__file__))
SCRATCH_DIR = os.path.join(TOP_DIR, "scratch")
LANGUAGE_CODE = "en"
NUM_TOP_WORDS = 50000
WORD_LENGTH_MIN = 4
WORD_LENGTH_MAX = 6
NGRAM_LENGTH_MIN = 2
NGRAM_LETTER_EMPTY = "█"
NGRAM_FREQUENCY_MIN = 30
