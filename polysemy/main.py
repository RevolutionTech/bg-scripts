import csv
import os

from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from wordfreq import top_n_list

from polysemy.constants import SCRATCH_DIR, MOST_COMMON_WORDS_REMOVED, MIN_NUM_DEFINITIONS


wnl = WordNetLemmatizer()


def is_canonical_lemma(word):
    synsets = wn.synsets(word)
    if not synsets:
        return False
    for synset in synsets:
        if synset.pos() == wn.VERB:
            # Prefer verbs if it's an option
            pos = wn.VERB
            break
    else:
        # If no verbs, just use the most common POS
        pos = synsets[0].pos()
    lemma = wnl.lemmatize(word, pos=pos)
    return lemma == word


def filter_lemmas(words):
    return {word for word in words if is_canonical_lemma(word)}


def filter_polysemous_words(words):
    return [
        (word, num_definitions) for word in words if (num_definitions := len(wn.synsets(word))) >= MIN_NUM_DEFINITIONS
    ]


def write_csv(words):
    filename = os.path.join(SCRATCH_DIR, "polysemous-words.csv")
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Word", "Num Definitions"])
        csvwriter.writerows(words)


def runscript():
    top_10000 = top_n_list("en", 10000)
    super_common_words = top_n_list("en", MOST_COMMON_WORDS_REMOVED)
    vocab = set(top_10000) - set(super_common_words)  # pretty common words, but not stuff like 'very' and 'when'
    vocab_lemmas = filter_lemmas(vocab)
    polysemous_lemmas = filter_polysemous_words(vocab_lemmas)
    sorted_words = sorted(polysemous_lemmas, key=lambda x: x[1], reverse=True)
    write_csv(sorted_words)


if __name__ == "__main__":
    runscript()
