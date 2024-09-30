from makepdf.sheet import BackType, Sheet


def make_telegram_pdfs():
    boards = Sheet("boards", 124, 200, padding=2, outer_margin=5, rotate_images=True, show_cut_lines=False)
    boards.generate_pdf()

    letters = Sheet("letters", 52, 72, back_type=BackType.UNIQUE, outer_margin=0, rotate_images=True)
    letters.generate_pdf()

    words = Sheet("words", 72, 52, back_type=BackType.UNIQUE, outer_margin=0)
    words.generate_pdf()

    goals = Sheet("goals", 72, 52, back_type=BackType.UNIQUE, outer_margin=0)
    goals.generate_pdf()

    solo = Sheet("solo", 52, 72, back_type=BackType.SHARED)
    solo.generate_pdf()


def make_category_matchmaker_pdfs():
    objects = Sheet("objects", 89, 62, back_type=BackType.SHARED, outer_margin=5, show_cut_lines=False)
    objects.generate_pdf()

    categories = Sheet("categories", 89, 62, back_type=BackType.SHARED, outer_margin=5, show_cut_lines=False)
    categories.generate_pdf()

    numbers = Sheet("numbers", 66, 33, back_type=BackType.UNIQUE, show_cut_lines=False)
    numbers.generate_pdf()


def runscript():
    make_telegram_pdfs()
    make_category_matchmaker_pdfs()


if __name__ == "__main__":
    runscript()
