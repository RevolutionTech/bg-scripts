import os

TOP_DIR = os.path.dirname(os.path.dirname(__file__))
SCRATCH_DIR = os.path.join(TOP_DIR, "scratch")
BASE_IMAGES_DIR = os.path.join(SCRATCH_DIR, "images")
BACK_IMAGE_FILENAME = "back"
IMAGE_EXT = "png"
DEFAULT_OUTER_MARGIN = 15

# A4 page size is deprecated, but kept for backwards compatibility. We should migrate all sheets to letter size.
PAGE_SIZE_A4 = "a4"  # deprecated
PAGE_SIZE_LETTER = "letter"
A4_PDF_WIDTH = 210  # https://stackoverflow.com/a/27327984/3241924
A4_PDF_HEIGHT = 297  # https://stackoverflow.com/a/27327984/3241924
LETTER_PDF_WIDTH = 216
LETTER_PDF_HEIGHT = 280
