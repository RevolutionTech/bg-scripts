import csv
import itertools
import os
from collections import Counter

from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from wordfreq import top_n_list

from polysemy.constants import SCRATCH_DIR, MOST_COMMON_WORDS_REMOVED, MIN_NUM_DEFINITIONS


sbert = SentenceTransformer("all-MiniLM-L6-v2")
wnl = WordNetLemmatizer()


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


def write_csv(words):
    filename = os.path.join(SCRATCH_DIR, "polysemous-words.csv")
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Word", "Num Definitions"])
        csvwriter.writerows(words)


def read_concrete_words():
    words = []

    filename = os.path.join(SCRATCH_DIR, "concrete-words.csv")
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for (word,) in csvreader:
            words.append(word)

    return words


def sbert_similarity(word, phrase):
    """Compute cosine similarity between a word and a phrase using SBERT."""
    word_vec = sbert.encode(word)
    phrase_vec = sbert.encode(phrase)
    return 1 - cosine(word_vec, phrase_vec)


def calculate_similarities(polysemous_words):
    concrete_words = read_concrete_words()

    filename = os.path.join(SCRATCH_DIR, "word-similarities.csv")
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Concrete Word", "Polysemous Word", "Similarity"])
        for word in concrete_words:
            for polysemous_word, _ in polysemous_words:
                try:
                    similarity = sbert_similarity(polysemous_word, word)
                except KeyError:
                    print(f"Could not find {word=} or {polysemous_word=}!")
                    continue

                csvwriter.writerow([word, polysemous_word, similarity])


def create_word_groupings(min_similarity, max_similarity, once_only=True):
    print(f"{min_similarity=} {max_similarity=}")

    # First we identify all of the matching similarities
    matching = set()
    filename = os.path.join(SCRATCH_DIR, "word-similarities.csv")
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        next(csvreader)  # skip header
        for *words, similarity in csvreader:
            if min_similarity <= float(similarity) <= max_similarity:
                matching.add(tuple(words))

    # Then we pick a polysemous word and eliminate all other concrete words that work well with it
    # Continue until all polysemous words have been picked
    concrete_words = set()
    banned_concrete_words = set()
    polysemous_words = set()
    for concrete_word, polysemous_word in matching:
        if len(polysemous_words) >= 10:
            break
        if concrete_word in banned_concrete_words:
            continue
        else:
            concrete_words.add(concrete_word)
            polysemous_words.add(polysemous_word)
            if once_only:
                for cw, pw in matching:
                    if pw == polysemous_word and cw != concrete_word:
                        banned_concrete_words.add(cw)

    print(f"{concrete_words=}")
    print(f"{polysemous_words=}")



def runscript():
    top_10000 = top_n_list("en", 10000)
    super_common_words = top_n_list("en", MOST_COMMON_WORDS_REMOVED)
    vocab = set(top_10000) - set(super_common_words)  # pretty common words, but not stuff like 'very' and 'when'
    vocab_lemmas = filter_lemmas(vocab)
    polysemous_lemmas = filter_polysemous_words(vocab_lemmas)
    sorted_words = sorted(polysemous_lemmas, key=lambda x: x[1], reverse=True)
    write_csv(sorted_words)
    calculate_similarities(sorted_words)
    create_word_groupings(0.325, 1)
    create_word_groupings(0.25, 0.3249)
    create_word_groupings(0, 0.2499, once_only=False)


if __name__ == "__main__":
    runscript()
