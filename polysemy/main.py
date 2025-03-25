from polysemy.concrete import read_concrete_words
from polysemy.similarity import calculate_similarities
from polysemy.sorted import generate_sorted_words


def runscript():
    concrete_words = read_concrete_words()
    sorted_words = generate_sorted_words()
    calculate_similarities(concrete_words, sorted_words)


if __name__ == "__main__":
    runscript()
