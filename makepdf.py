import os

from fpdf import FPDF

SCRATCH_DIR = "scratch"
IMAGES_DIR = os.path.join(SCRATCH_DIR, "images")
IMAGE_EXT = "png"
PAGE_WIDTH = 210  # https://stackoverflow.com/a/27327984/3241924
PAGE_HEIGHT = 297  # https://stackoverflow.com/a/27327984/3241924
MIN_OUTER_MARGIN = 15
IMAGE_WIDTH = 84
IMAGE_HEIGHT = 60


def get_images(dir):
    for filename in sorted(os.listdir(dir)):
        name, ext = os.path.splitext(filename)
        if ext == f".{IMAGE_EXT}":
            yield filename


def runscript():
    print("Generating PDF...")
    page_num_rows = (PAGE_HEIGHT - 2 * MIN_OUTER_MARGIN) // IMAGE_HEIGHT
    page_num_cols = (PAGE_WIDTH - 2 * MIN_OUTER_MARGIN) // IMAGE_WIDTH
    hor_margin = (PAGE_WIDTH - (page_num_cols * IMAGE_WIDTH)) // 2
    vert_margin = (PAGE_HEIGHT - (page_num_rows * IMAGE_HEIGHT)) // 2
    images_per_page = page_num_rows * page_num_cols

    pdf = FPDF()
    for i, filename in enumerate(get_images(IMAGES_DIR)):
        full_filename = os.path.join(IMAGES_DIR, filename)

        image_for_page = i % images_per_page
        row = image_for_page // page_num_cols
        column = image_for_page % page_num_cols
        if image_for_page == 0:
            pdf.add_page()

        pdf.image(
            full_filename,
            hor_margin + column * IMAGE_WIDTH,
            vert_margin + row * IMAGE_HEIGHT,
            IMAGE_WIDTH,
            IMAGE_HEIGHT,
        )
    pdf.output(os.path.join(SCRATCH_DIR, "output.pdf"), "F")

    print("PDF generated successfully!")


if __name__ == "__main__":
    runscript()
