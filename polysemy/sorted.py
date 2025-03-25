import csv
import itertools
import os
from collections import Counter

from nltk.corpus import wordnet as wn

from polysemy.common import get_common_words
from polysemy.constants import SCRATCH_DIR, MIN_NUM_DEFINITIONS
from polysemy.csvreader import read_word_list


def is_canonical_lemma(word):
    synsets = wn.synsets(word)
    if not synsets:
        return False
    lemma_counts = Counter(itertools.chain.from_iterable([synset.lemma_names() for synset in synsets]))
    most_common_form = lemma_counts.most_common(1)[0][0]
    return word == most_common_form


def filter_lemmas(words):
    return {word for word in words if is_canonical_lemma(word)}


def filter_polysemous_words(words):
    return [
        (word, num_definitions) for word in words if (num_definitions := len(wn.synsets(word))) >= MIN_NUM_DEFINITIONS
    ]


def write_csv(filename, words):
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Word", "Num Definitions"])
        csvwriter.writerows(words)


def generate_sorted_words(out_filename):
    vocab = get_common_words()
    vocab_lemmas = filter_lemmas(vocab)
    polysemous_lemmas = filter_polysemous_words(vocab_lemmas)
    sorted_words = sorted(polysemous_lemmas, key=lambda x: x[1], reverse=True)
    write_csv(out_filename, sorted_words)
    return [word for word, _ in sorted_words]


def read_or_generate_sorted_words():
    filename = os.path.join(SCRATCH_DIR, "polysemous-words.csv")
    if os.path.exists(filename):
        return read_word_list(filename)
    else:
        return generate_sorted_words(filename)
