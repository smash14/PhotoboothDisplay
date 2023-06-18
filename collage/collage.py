import sys
import os.path
from PIL import Image, ImageOps
import logging


class Collage:
    def __init__(self, picture_list, background_path="images/background.jpg", width=6048, height=4032, margin_border=5, margin_bottom=8):
        self.background_path = background_path
        self.width = width
        self.height = height
        self._open_or_create_background_image()
        self.picture_list = picture_list

        self.margin_border = margin_border
        self.margin_bottom = margin_bottom

        # self.ratio = width / height  # aspect ratio of background picture
        self.margin_width = int(self.width * self.margin_border / 100)
        self.margin_height = int(self.height * self.margin_border / 100)
        self.margin_bottom = int(self.height * self.margin_bottom / 100)

    @staticmethod
    def _resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def _open_or_create_background_image(self):
        if os.path.isfile(self.background_path):
            self.background = Image.open(self.background_path)
            bg_width, bg_height = self.background.size
            if bg_width != self.width or bg_height != self.height:
                logging.info(f"Provided Background size does not fit to target size. Will resize background image for you \r\n"
                             f"Background size: {bg_width} x {bg_height}, target size: {self.width} x {self.height}")
                self.background = ImageOps.fit(self.background, (self.width, self.height))
        else:
            logging.warning(f"Could not find Background image {self.background_path}. Will create a white background for you")
            self.background = Image.new("RGB", (self.width, self.height), "white")

    def _create_collage_list(self, amount, width, height):
        """
        Creates a list containing actual images using the picture_list with the correct width and height.
        Automatically creates a placeholder image if not enough images available in list
        :param amount: amount of files which should be in the collage list
        :param width: target width of each collage picture
        :param height: target height of each collage picture
        :return: list of images with correct width and height
        """
        collage_list = []
        # Create a list of collage pictures with correct width and height and crop image according to margins
        for x in range(-1, (amount + 1) * -1, -1):
            try:
                img_collage = Image.open(self.picture_list[x])
            except IndexError:
                # TODO: Alpha channel seems not to work, image becomes black
                img_collage = Image.new("RGB", (10, 10), "white")
            except FileNotFoundError:
                logging.error(f"Error: Could not find picture in picture list: {self.picture_list[x]}")
                img_collage = Image.new("RGB", (10, 10), "white")
            img_collage = ImageOps.fit(img_collage, (width, height))
            collage_list.append(img_collage)
        return collage_list

    def create_collage_2x2(self):
        # calculate width and height of each single collage picture according to border margin and bottom margin
        collage_picture_width = int(self.width / 2 - self.margin_width - 0.5 * self.margin_width)
        collage_picture_height = int(self.height / 2 - self.margin_height
                                     - 0.5 * self.margin_height - self.margin_bottom)

        collage_list = self._create_collage_list(4, collage_picture_width, collage_picture_height)

        # take background image and paste each collage image on top of it with correct margin
        self.background.paste(collage_list[0], (self.margin_width, self.margin_height))  # top left
        self.background.paste(collage_list[1], (self.width - collage_picture_width - self.margin_width, self.margin_height))  # top right
        self.background.paste(collage_list[2], (self.margin_width, self.margin_height * 2 + collage_picture_height))  # bottom left
        self.background.paste(collage_list[3], (self.margin_width * 2 + collage_picture_width, self.margin_height * 2 + collage_picture_height))  # bottom right

    def create_collage_1x1(self):
        # calculate width and height of each single collage picture according to border margin and bottom margin
        collage_picture_width = int(self.width - 2 * self.margin_width)
        collage_picture_height = int(self.height - 2 * self.margin_height - self.margin_bottom)

        collage_list = self._create_collage_list(1, collage_picture_width, collage_picture_height)

        # take background image and paste each collage image on top of it with correct margin
        self.background.paste(collage_list[0], (self.margin_width, self.margin_height))  # top left

    def show_collage(self):
        self.background.show()

    def save_collage(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.background.save(file_path, quality=95)
