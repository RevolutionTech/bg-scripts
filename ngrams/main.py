from ngrams.generator import NgramGenerator
from ngrams.writer import NgramWriter


def runscript():
    ngrams = NgramGenerator()
    ngrams.generate()

    writer = NgramWriter(ngrams)
    writer.write_letter_counts()
    writer.write_all_ngrams()


if __name__ == "__main__":
    runscript()
