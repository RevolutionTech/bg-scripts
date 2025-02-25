import csv
import enum
import math
import os
import tempfile
from collections import defaultdict
from typing import Optional, Tuple

from PIL import Image
from fpdf import FPDF

from makepdf.constants import (
    SCRATCH_DIR, BASE_IMAGES_DIR, BACK_IMAGE_FILENAME, IMAGE_EXT, PAGE_SIZE_LETTER, PAGE_WIDTH, PAGE_HEIGHT,
    DEFAULT_OUTER_MARGIN
)


class BackType(enum.Enum):
    NONE = "none"
    SHARED = "shared"
    UNIQUE = "unique"


class Sheet:
    def __init__(
            self,
            image_group: str,
            image_type: str,
            image_width: int,
            image_height: int,
            cut_width: Optional[int] = None,
            cut_height: Optional[int] = None,
            padding: int = 0,
            back_type: BackType = BackType.NONE,
            outer_margin: int = DEFAULT_OUTER_MARGIN,
            rotate_images: bool = False,
            bleed_color: Optional[Tuple[int, int, int]] = None,
            show_cut_lines: bool = True
    ):
        self.output_filename = f"{image_type}.pdf"
        self.images_dir = os.path.join(BASE_IMAGES_DIR, image_group, image_type)
        self.back_type = back_type

        self.image_width = image_height if rotate_images else image_width
        self.image_height = image_width if rotate_images else image_height
        self.padding = padding
        self.rotate_images = rotate_images
        self.bleed_color = bleed_color
        self.show_cut_lines = show_cut_lines
        self.cut_width = (cut_height if rotate_images else cut_width) or self.image_width
        self.cut_height = (cut_width if rotate_images else cut_height) or self.image_height

        self.page_num_rows = (PAGE_HEIGHT - 2 * outer_margin) // (self.cut_height + self.padding)
        self.page_num_cols = (PAGE_WIDTH - 2 * outer_margin) // (self.cut_width + self.padding)
        self.hor_margin = (
            PAGE_WIDTH - (self.page_num_cols * self.cut_width + (self.page_num_cols - 1) * self.padding)
        ) // 2
        self.vert_margin = (
            PAGE_HEIGHT - (self.page_num_rows * self.cut_height + (self.page_num_rows - 1) * self.padding)
        ) // 2
        self.images_per_page = self.page_num_rows * self.page_num_cols

        self.pdf = FPDF(format=PAGE_SIZE_LETTER)

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

        image_requires_crop = self.cut_width != self.image_width or self.cut_height != self.image_height
        image_requires_alteration = image_requires_crop or self.rotate_images
        with tempfile.NamedTemporaryFile() as f:
            if image_requires_alteration:
                with Image.open(full_filename) as im:
                    full_filename = f"{f.name}.{IMAGE_EXT}"
                    if self.rotate_images:
                        im = im.rotate(90 if reverse else -90, expand=True)
                    if image_requires_crop:
                        assert round(im.width / self.image_width, 1) == round(im.height / self.image_height, 1)
                        pixels_to_points_ratio = round(im.width / self.image_width, 1)
                        cut_margin_width = math.floor(
                            pixels_to_points_ratio * ((self.image_width - self.cut_width) / 2)
                        )
                        cut_margin_height = math.floor(
                            pixels_to_points_ratio * ((self.image_height - self.cut_height) / 2)
                        )
                        im = im.crop(
                            (
                                cut_margin_width,
                                cut_margin_height,
                                im.width - cut_margin_width,
                                im.height - cut_margin_height,
                            )
                        )
                    im.save(full_filename)

            self.pdf.image(
                full_filename,
                self.hor_margin + column * (self.cut_width + self.padding),
                self.vert_margin + row * (self.cut_height + self.padding),
                self.cut_width,
                self.cut_height,
            )

    def _add_bleed_color_to_pdf(self):
        if self.bleed_color:
            self.pdf.set_fill_color(*self.bleed_color)
            self.pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, "F")
            self.pdf.set_fill_color(0)

    def _add_cut_lines_to_pdf(self):
        if self.show_cut_lines:
            for row_line in range(self.page_num_rows + 1):
                line_y = self.vert_margin + row_line * (self.cut_height + self.padding) - self.padding // 2

                # Skip cut lines at the edge of the page
                if line_y in (0, PAGE_HEIGHT):
                    continue

                self.pdf.line(0, line_y, PAGE_WIDTH, line_y)
            for col_line in range(self.page_num_cols + 1):
                line_x = self.hor_margin + col_line * (self.cut_width + self.padding) - self.padding // 2

                # Skip cut lines at the edge of the page
                if line_x in (0, PAGE_WIDTH):
                    continue

                self.pdf.line(line_x, 0, line_x, PAGE_HEIGHT)

    def _add_back_page(self, filenames):
        self.pdf.add_page()
        self._add_bleed_color_to_pdf()
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
                    self._add_bleed_color_to_pdf()

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

        self.pdf.output(os.path.join(self.images_dir, self.output_filename), "F")

        print("PDF generated successfully!")
