from makepdf.sheet import Orientation, BackType, Sheet


def runscript():
    boards = Sheet("boards", 238, 135, orientation=Orientation.LANDSCAPE, padding=0)
    boards.generate_pdf()

    letters = Sheet("letters", 60, 84, back_type=BackType.SHARED)
    letters.generate_pdf()

    words = Sheet("words", 84, 60, back_type=BackType.SHARED)
    words.generate_pdf()

    goals = Sheet("goals", 84, 60, back_type=BackType.UNIQUE)
    goals.generate_pdf()


if __name__ == "__main__":
    runscript()
