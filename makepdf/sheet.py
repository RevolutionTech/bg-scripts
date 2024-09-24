import csv
import enum
import os
from collections import defaultdict

from fpdf import FPDF

from makepdf.constants import (
    SCRATCH_DIR, BASE_IMAGES_DIR, BACK_IMAGE_FILENAME, IMAGE_EXT, PAGE_SIZE_LETTER, PAGE_WIDTH, PAGE_HEIGHT,
    DEFAULT_OUTER_MARGIN
)


class Orientation(enum.Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class BackType(enum.Enum):
    NONE = "none"
    SHARED = "shared"
    UNIQUE = "unique"


class Sheet:
    def __init__(
            self,
            image_type: str,
            image_width: int,
            image_height: int,
            orientation: Orientation = Orientation.PORTRAIT,
            padding: int = 0,
            back_type: BackType = BackType.NONE,
            outer_margin: int = DEFAULT_OUTER_MARGIN,
            show_cut_lines: bool = True
    ):
        self.output_filename = f"{image_type}.pdf"
        self.images_dir = os.path.join(BASE_IMAGES_DIR, image_type)
        self.back_type = back_type

        self.image_width = image_width
        self.image_height = image_height
        self.padding = padding
        self.show_cut_lines = show_cut_lines

        self.page_height = PAGE_HEIGHT if orientation == Orientation.PORTRAIT else PAGE_WIDTH
        self.page_width = PAGE_WIDTH if orientation == Orientation.PORTRAIT else PAGE_HEIGHT
        self.page_num_rows = (self.page_height - 2 * outer_margin) // (self.image_height + self.padding)
        self.page_num_cols = (self.page_width - 2 * outer_margin) // (self.image_width + self.padding)
        self.hor_margin = (
            self.page_width - (self.page_num_cols * self.image_width + (self.page_num_cols - 1) * self.padding)
        ) // 2
        self.vert_margin = (
            self.page_height - (self.page_num_rows * self.image_height + (self.page_num_rows - 1) * self.padding)
        ) // 2
        self.images_per_page = self.page_num_rows * self.page_num_cols

        self.pdf = FPDF(orientation=orientation.value, format=PAGE_SIZE_LETTER)

    def _get_quantities(self):
        quantities = defaultdict(lambda: 1)

        filename = os.path.join(self.images_dir, "quantity.csv")
        try:
            with open(filename, "r") as f:
                csvreader = csv.reader(f)
                next(csvreader)  # skip headers
                for card_id, quantity in csvreader:
                    quantities[card_id] = int(quantity)
        except FileNotFoundError:
            pass  # no explicit quantities provided, use default

        return quantities

    def _get_images(self):
        for filename in sorted(os.listdir(self.images_dir)):
            name, ext = os.path.splitext(filename)
            if ext == f".{IMAGE_EXT}" and (self.back_type != BackType.SHARED or name != BACK_IMAGE_FILENAME):
                yield filename

    def _add_image_to_pdf(self, image_for_page: int, full_filename: str, reverse: bool = False):
        row = image_for_page // self.page_num_cols
        column = image_for_page % self.page_num_cols
        if reverse:
            # Print images on reverse from right to left
            column = self.page_num_cols - column - 1
        self.pdf.image(
            full_filename,
            self.hor_margin + column * (self.image_width + self.padding),
            self.vert_margin + row * (self.image_height + self.padding),
            self.image_width,
            self.image_height,
        )

    def _add_cut_lines_to_pdf(self):
        if self.show_cut_lines:
            for row_line in range(self.page_num_rows + 1):
                line_y = self.vert_margin + row_line * (self.image_height + self.padding) - self.padding // 2

                # Skip cut lines at the end of the page
                if line_y in (0, self.page_height):
                    continue

                self.pdf.line(0, line_y, self.page_width, line_y)
            for col_line in range(self.page_num_cols + 1):
                line_x = self.hor_margin + col_line * (self.image_width + self.padding) - self.padding // 2

                # Skip cut lines at the end of the page
                if line_x in (0, self.page_width):
                    continue

                self.pdf.line(line_x, 0, line_x, self.page_height)

    def _add_back_page(self, filenames):
        self.pdf.add_page()
        for i, filename in enumerate(filenames):
            if self.back_type == BackType.UNIQUE:
                back_filename = os.path.join(self.images_dir, BACK_IMAGE_FILENAME, filename)
            else:
                back_filename = os.path.join(self.images_dir, f"{BACK_IMAGE_FILENAME}.png")
            self._add_image_to_pdf(i, back_filename, reverse=True)

    def generate_pdf(self):
        quantities = self._get_quantities()

        print(f"Generating PDF {self.output_filename}...")

        i = 0
        is_page_end = False
        filenames_for_back = []
        for filename in self._get_images():
            card_id, _ = os.path.splitext(filename)
            full_filename = os.path.join(self.images_dir, filename)

            quantity = quantities[card_id]
            for _ in range(quantity):
                # Handle the start of a page
                is_page_start = i % self.images_per_page == 0
                if is_page_start:
                    self.pdf.add_page()

                # Insert a card into the page
                image_for_page = i % self.images_per_page
                self._add_image_to_pdf(image_for_page, full_filename)
                filenames_for_back.append(filename)

                # Handle the end of a page
                i += 1
                is_page_end = i % self.images_per_page == 0
                if is_page_end:
                    self._add_cut_lines_to_pdf()
                    if self.back_type != BackType.NONE:
                        self._add_back_page(filenames_for_back)
                    filenames_for_back = []

        # Final partial final page
        if not is_page_end:
            self._add_cut_lines_to_pdf()
            if self.back_type != BackType.NONE:
                self._add_back_page(filenames_for_back)

        self.pdf.output(os.path.join(SCRATCH_DIR, self.output_filename), "F")

        print("PDF generated successfully!")
