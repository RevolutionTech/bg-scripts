import os

TOP_DIR = os.path.dirname(os.path.dirname(__file__))
SCRATCH_DIR = os.path.join(TOP_DIR, "scratch")
BASE_IMAGES_DIR = os.path.join(SCRATCH_DIR, "images")
BACK_IMAGE_FILENAME = "back"
IMAGE_EXT = "png"
PAGE_WIDTH = 210  # https://stackoverflow.com/a/27327984/3241924
PAGE_HEIGHT = 297  # https://stackoverflow.com/a/27327984/3241924
MIN_OUTER_MARGIN = 15
