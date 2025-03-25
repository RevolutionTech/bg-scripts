from polysemy.csvreader import read_word_list
from polysemy.similarity import calculate_similarities
from polysemy.sorted import read_or_generate_sorted_words


def runscript():
    concrete_words = read_word_list("concrete-words.csv")
    sorted_words = read_or_generate_sorted_words()
    calculate_similarities(concrete_words, sorted_words)


if __name__ == "__main__":
    runscript()
