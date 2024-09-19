from makepdf.sheet import Orientation, BackType, Sheet


def make_telegram_pdfs():
    boards = Sheet("boards", 124, 200, orientation=Orientation.LANDSCAPE, padding=2, outer_margin=5)
    boards.generate_pdf()

    letters = Sheet("letters", 62, 89, back_type=BackType.UNIQUE, outer_margin=5)
    letters.generate_pdf()

    words = Sheet("words", 89, 62, back_type=BackType.UNIQUE, outer_margin=5)
    words.generate_pdf()

    goals = Sheet("goals", 89, 62, back_type=BackType.UNIQUE, outer_margin=5)
    goals.generate_pdf()

    solo = Sheet("solo", 62, 89, back_type=BackType.SHARED)
    solo.generate_pdf()


def make_category_matchmaker_pdfs():
    objects = Sheet("objects", 89, 62, back_type=BackType.SHARED, outer_margin=5)
    objects.generate_pdf()

    categories = Sheet("categories", 89, 62, back_type=BackType.SHARED, outer_margin=5)
    categories.generate_pdf()

    numbers = Sheet("numbers", 66, 33, back_type=BackType.UNIQUE)
    numbers.generate_pdf()


def runscript():
    make_telegram_pdfs()
    make_category_matchmaker_pdfs()


if __name__ == "__main__":
    runscript()
