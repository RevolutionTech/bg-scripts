import csv
import os

from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

from polysemy.constants import SCRATCH_DIR


sbert = SentenceTransformer("all-MiniLM-L6-v2")


def sbert_similarity(word, phrase):
    """Compute cosine similarity between a word and a phrase using SBERT."""
    word_vec = sbert.encode(word)
    phrase_vec = sbert.encode(phrase)
    return 1 - cosine(word_vec, phrase_vec)


def calculate_similarities(concrete_words, polysemous_words):
    filename = os.path.join(SCRATCH_DIR, "word-similarities.csv")
    with open(filename, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Concrete Word", "Polysemous Word", "Similarity"])
        for word in concrete_words:
            for polysemous_word in polysemous_words:
                try:
                    similarity = sbert_similarity(polysemous_word, word)
                except KeyError:
                    print(f"Could not find {word=} or {polysemous_word=}!")
                    continue

                csvwriter.writerow([word, polysemous_word, similarity])
