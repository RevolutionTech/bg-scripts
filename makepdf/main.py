from makepdf.sheet import Sheet


def runscript():
    boards = Sheet("boards", 144, 108, padding=15)
    boards.generate_pdf()

    letters = Sheet("letters", 60, 84, has_back=True)
    letters.generate_pdf()

    words = Sheet("words", 84, 60, has_back=True)
    words.generate_pdf()


if __name__ == "__main__":
    runscript()
