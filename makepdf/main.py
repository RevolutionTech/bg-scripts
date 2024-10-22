from makepdf.sheet import BackType, Sheet


def make_telegram_pdfs():
    boards = Sheet(
        "boards", 124, 200, back_type=BackType.SHARED, padding=2, outer_margin=5,
        rotate_images=True, show_cut_lines=False
    )
    boards.generate_pdf()

    letters = Sheet(
        "letters", 69, 94, back_type=BackType.UNIQUE, outer_margin=0,
        rotate_images=True, cut_line_width=64, cut_line_height=89
    )
    letters.generate_pdf()

    words = Sheet("words", 94, 69, back_type=BackType.UNIQUE, outer_margin=0, cut_line_width=89, cut_line_height=64)
    words.generate_pdf()

    goals = Sheet("goals", 94, 69, back_type=BackType.UNIQUE, outer_margin=0, cut_line_width=89, cut_line_height=64)
    goals.generate_pdf()

    solo = Sheet("solo", 69, 94, back_type=BackType.SHARED, cut_line_width=64, cut_line_height=89)
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
