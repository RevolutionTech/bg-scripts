from makepdf.sheet import BackType, Sheet


def make_telegram_pdfs():
    boards = Sheet(
        "boards", image_width=124, image_height=200, back_type=BackType.SHARED, padding=2, outer_margin=5,
        rotate_images=True, show_cut_lines=False
    )
    boards.generate_pdf()

    letters = Sheet(
        "letters", image_width=69, image_height=94, back_type=BackType.UNIQUE, outer_margin=0,
        rotate_images=True, cut_width=64, cut_height=89
    )
    letters.generate_pdf()

    words = Sheet(
        "words", image_width=94, image_height=69, cut_width=89, cut_height=64, back_type=BackType.UNIQUE, outer_margin=0
    )
    words.generate_pdf()

    goals = Sheet(
        "goals", image_width=94, image_height=69, cut_width=89, cut_height=64, back_type=BackType.UNIQUE, outer_margin=0
    )
    goals.generate_pdf()

    solo = Sheet("solo", image_width=69, image_height=94, cut_width=64, cut_height=89, back_type=BackType.SHARED)
    solo.generate_pdf()


def make_category_matchmaker_pdfs():
    objects = Sheet(
        "objects", image_width=89, image_height=62, back_type=BackType.SHARED, outer_margin=5, show_cut_lines=False
    )
    objects.generate_pdf()

    categories = Sheet(
        "categories", image_width=89, image_height=62, back_type=BackType.SHARED, outer_margin=5, show_cut_lines=False
    )
    categories.generate_pdf()

    numbers = Sheet("numbers", image_width=66, image_height=33, back_type=BackType.UNIQUE, show_cut_lines=False)
    numbers.generate_pdf()


def runscript():
    make_telegram_pdfs()
    make_category_matchmaker_pdfs()


if __name__ == "__main__":
    runscript()
