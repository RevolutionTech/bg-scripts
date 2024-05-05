import csv
import os
from collections import defaultdict

from fpdf import FPDF

from makepdf.constants import SCRATCH_DIR, BASE_IMAGES_DIR, IMAGE_EXT, PAGE_WIDTH, PAGE_HEIGHT, MIN_OUTER_MARGIN


class Sheet:
    def __init__(self, image_type: str, image_width: int, image_height: int, padding: int = 0):
        self.output_filename = f"{image_type}.pdf"
        self.images_dir = os.path.join(BASE_IMAGES_DIR, image_type)

        self.image_width = image_width
        self.image_height = image_height
        self.padding = padding

        self.page_num_rows = (PAGE_HEIGHT - 2 * MIN_OUTER_MARGIN) // (self.image_height + self.padding)
        self.page_num_cols = (PAGE_WIDTH - 2 * MIN_OUTER_MARGIN) // (self.image_width + self.padding)
        self.hor_margin = (PAGE_WIDTH - (self.page_num_cols * (self.image_width + self.padding))) // 2
        self.vert_margin = (PAGE_HEIGHT - (self.page_num_rows * (self.image_height + self.padding))) // 2
        self.images_per_page = self.page_num_rows * self.page_num_cols

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
            if ext == f".{IMAGE_EXT}":
                yield filename

    def generate_pdf(self):
        quantities = self._get_quantities()

        print(f"Generating PDF {self.output_filename}...")

        i = 0
        pdf = FPDF()
        for filename in self._get_images():
            card_id, _ = os.path.splitext(filename)
            full_filename = os.path.join(self.images_dir, filename)

            quantity = quantities[card_id]
            for _ in range(quantity):
                image_for_page = i % self.images_per_page
                row = image_for_page // self.page_num_cols
                column = image_for_page % self.page_num_cols
                if image_for_page == 0:
                    pdf.add_page()

                pdf.image(
                    full_filename,
                    self.hor_margin + column * (self.image_width + self.padding),
                    self.vert_margin + row * (self.image_height + self.padding),
                    self.image_width,
                    self.image_height,
                )
                i += 1
        pdf.output(os.path.join(SCRATCH_DIR, self.output_filename), "F")

        print("PDF generated successfully!")
