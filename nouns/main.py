import random

from wordfreq import iter_wordlist as iter_wikipedia_wordlist


def runscript():
    valid_words = set()

    for word in iter_wikipedia_wordlist("en"):
        valid_words.add(word)
        if all(letter.isascii() and letter.isalpha() and letter.islower() for letter in word):
            valid_words.add(word)

            if len(valid_words) >= 10000:
                break

    selected_words = random.sample(valid_words, 100)
    for word in selected_words:
        print(word)


if __name__ == "__main__":
    runscript()
