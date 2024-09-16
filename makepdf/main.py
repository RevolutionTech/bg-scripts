from makepdf.sheet import Orientation, BackType, Sheet


def make_telegram_pdfs():
    boards = Sheet("boards", 138, 179, orientation=Orientation.LANDSCAPE, padding=2, outer_margin=5)
    boards.generate_pdf()

    letters = Sheet("letters", 60, 84, back_type=BackType.UNIQUE)
    letters.generate_pdf()

    words = Sheet("words", 84, 60, back_type=BackType.UNIQUE)
    words.generate_pdf()

    goals = Sheet("goals", 84, 60, back_type=BackType.UNIQUE)
    goals.generate_pdf()


def make_category_matchmaker_pdfs():
    objects = Sheet("objects", 84, 60, back_type=BackType.SHARED)
    objects.generate_pdf()

    categories = Sheet("categories", 84, 60, back_type=BackType.SHARED)
    categories.generate_pdf()

    numbers = Sheet("numbers", 64, 32, back_type=BackType.UNIQUE)
    numbers.generate_pdf()


def runscript():
    make_telegram_pdfs()
    make_category_matchmaker_pdfs()


if __name__ == "__main__":
    runscript()
