import csv
import os
from collections import defaultdict

from fpdf import FPDF

SCRATCH_DIR = "scratch"
BASE_IMAGES_DIR = os.path.join(SCRATCH_DIR, "images")
IMAGE_EXT = "png"
PAGE_WIDTH = 210  # https://stackoverflow.com/a/27327984/3241924
PAGE_HEIGHT = 297  # https://stackoverflow.com/a/27327984/3241924
MIN_OUTER_MARGIN = 15


def get_images(dir: str):
    for filename in sorted(os.listdir(dir)):
        name, ext = os.path.splitext(filename)
        if ext == f".{IMAGE_EXT}":
            yield filename


def get_quantities(dir: str):
    quantities = defaultdict(lambda: 1)

    filename = os.path.join(dir, "quantity.csv")
    try:
        with open(filename, "r") as f:
            csvreader = csv.reader(f)
            next(csvreader)  # skip headers
            for card_id, quantity in csvreader:
                quantities[card_id] = int(quantity)
    except FileNotFoundError:
        pass  # no explicit quantities provided, use default

    return quantities


def generate_pdf(image_type: str, image_width: int, image_height: int):
    output_filename = f"{image_type}.pdf"
    images_dir = os.path.join(BASE_IMAGES_DIR, image_type)
    page_num_rows = (PAGE_HEIGHT - 2 * MIN_OUTER_MARGIN) // image_height
    page_num_cols = (PAGE_WIDTH - 2 * MIN_OUTER_MARGIN) // image_width
    hor_margin = (PAGE_WIDTH - (page_num_cols * image_width)) // 2
    vert_margin = (PAGE_HEIGHT - (page_num_rows * image_height)) // 2
    images_per_page = page_num_rows * page_num_cols

    quantities = get_quantities(images_dir)

    print(f"Generating PDF {output_filename}...")

    i = 0
    pdf = FPDF()
    for filename in get_images(images_dir):
        card_id, _ = os.path.splitext(filename)
        full_filename = os.path.join(images_dir, filename)

        quantity = quantities[card_id]
        for _ in range(quantity):
            image_for_page = i % images_per_page
            row = image_for_page // page_num_cols
            column = image_for_page % page_num_cols
            if image_for_page == 0:
                pdf.add_page()

            pdf.image(
                full_filename,
                hor_margin + column * image_width,
                vert_margin + row * image_height,
                image_width,
                image_height,
            )
            i += 1
    pdf.output(os.path.join(SCRATCH_DIR, output_filename), "F")

    print("PDF generated successfully!")


if __name__ == "__main__":
    generate_pdf("letters", 60, 84)
    generate_pdf("words", 84, 60)
