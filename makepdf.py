import os

from fpdf import FPDF

SCRATCH_DIR = "scratch"
IMAGES_DIR = os.path.join(SCRATCH_DIR, "images")
IMAGE_EXT = "png"
PAGE_WIDTH = 210  # https://stackoverflow.com/a/27327984/3241924
PAGE_HEIGHT = 297  # https://stackoverflow.com/a/27327984/3241924
IMAGES_PER_PAGE = 8
OUTER_MARGIN = 21
IMAGE_WIDTH = 84
IMAGE_HEIGHT = 60

def get_images(dir):
    for filename in sorted(os.listdir(dir)):
        name, ext = os.path.splitext(filename)
        if ext == f".{IMAGE_EXT}":
            yield filename

def runscript():
    print("Generating PDF...")

    pdf = FPDF()
    for i, filename in enumerate(get_images(IMAGES_DIR)):
        full_filename = os.path.join(IMAGES_DIR, filename)

        image_for_page = i % IMAGES_PER_PAGE
        row = image_for_page // 2
        column = image_for_page % 2
        if image_for_page == 0:
            pdf.add_page()

        pdf.image(full_filename, OUTER_MARGIN + column * IMAGE_WIDTH, OUTER_MARGIN + row * IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT)
    pdf.output(os.path.join(SCRATCH_DIR, "output.pdf"), "F")

    print("PDF generated successfully!")

if __name__ == "__main__":
    runscript()
