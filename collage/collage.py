import sys
import os.path
from PIL import Image, ImageOps, ImageEnhance
import logging


class Collage:
    def __init__(self, picture_list, background_path="images/background.jpg", width=6048, height=4032, margin_border=5,
                 margin_bottom=8, brightness_factor=1, contrast_factor=1, foreground_path=None):
        self.background = None
        self.foreground = None
        self.width = width
        self.height = height
        self.collage_picture = Image.new("RGBA", (self.width, self.height), "white")
        self._open_or_create_background_image(background_path)
        self._open_or_create_foreground_image(foreground_path)
        self.picture_list = picture_list

        self.margin_border = margin_border
        self.margin_bottom = margin_bottom

        # Image enhacements for brightness and contrast
        self.brightness_factor = brightness_factor
        self.contrast_factor = contrast_factor

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

    def _open_or_create_background_image(self, background_path):
        if background_path is not None:
            if os.path.isfile(background_path):
                self.background = Image.open(background_path)
                bg_width, bg_height = self.background.size
                if bg_width != self.width or bg_height != self.height:
                    logging.info(f"Provided Background size does not fit to target size. Will resize background image for you \r\n"
                                 f"Background size: {bg_width} x {bg_height}, target size: {self.width} x {self.height}")
                    self.background = ImageOps.fit(self.background, (self.width, self.height))
            else:
                logging.warning(f"Could not find Background image {background_path}. Will create a white background for you")
                self.background = Image.new("RGBA", (self.width, self.height), "white")
        else:
            self.background = Image.new("RGBA", (self.width, self.height), "white")

    def _open_or_create_foreground_image(self, foreground_path):
        if foreground_path is not None:
            if os.path.isfile(foreground_path):
                self.foreground = Image.open(foreground_path)
                fg_width, fg_height = self.foreground.size
                if fg_width != self.width or fg_height != self.height:
                    logging.info(f"Provided Foreground size does not fit to target size. Will resize background image for you \r\n"
                                 f"Foreground size: {fg_width} x {fg_height}, target size: {self.width} x {self.height}")
                    self.foreground = ImageOps.fit(self.background, (self.width, self.height))
            else:
                logging.warning(f"Could not find Foreground image {foreground_path}")

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
                logging.warning(f"Index error while creating collage. Maybe not enough photos until now.")
                img_collage = Image.new("RGBA", (10, 10), "white")
            except FileNotFoundError:
                logging.error(f"Error: Could not find picture in picture list: {self.picture_list[x]}")
                img_collage = Image.new("RGBA", (10, 10), "white")
            except Exception as e:
                logging.error(f"Unknown Error: {e}")
                logging.info(f"Create empty image for you")
                img_collage = Image.new("RGBA", (10, 10), "white")
            try:
                # Apply enhancements for brightness and contrast
                enhancer_brightness = ImageEnhance.Brightness(img_collage)
                img_enhanced_brightness = enhancer_brightness.enhance(self.brightness_factor)
                enhancer_contrast = ImageEnhance.Contrast(img_enhanced_brightness)
                img_enhanced_contrast = enhancer_contrast.enhance(self.contrast_factor)

                # Fit image to collage size
                img_collage = ImageOps.fit(img_enhanced_contrast, (width, height))
                collage_list.append(img_collage)
            except Exception as e:
                logging.error(f"Create fallback image due to unhandled exception: {e}")
                img_collage = Image.new("RGBA", (10, 10), "black")
                img_collage = ImageOps.fit(img_collage, (width, height))
                collage_list.append(img_collage)
        return collage_list

    def create_collage_2x2(self):
        # calculate width and height of each single collage picture according to border margin and bottom margin
        collage_picture_width = int(self.width / 2 - self.margin_width - 0.5 * self.margin_width)
        collage_picture_height = int(self.height / 2 - self.margin_height
                                     - 0.5 * self.margin_height - self.margin_bottom * 0.5)

        collage_list = self._create_collage_list(4, collage_picture_width, collage_picture_height)

        self.collage_picture.paste(self.background)

        # take background image and paste each collage image on top of it with correct margin
        self.collage_picture.paste(collage_list[0], (self.margin_width, self.margin_height))  # top left
        self.collage_picture.paste(collage_list[1], (self.width - collage_picture_width - self.margin_width, self.margin_height))  # top right
        self.collage_picture.paste(collage_list[2], (self.margin_width, self.margin_height * 2 + collage_picture_height))  # bottom left
        self.collage_picture.paste(collage_list[3], (self.margin_width * 2 + collage_picture_width, self.margin_height * 2 + collage_picture_height))  # bottom right

        if self.foreground is not None:
            self.collage_picture.paste(self.foreground, mask=self.foreground)

    def create_collage_1x1(self):
        # calculate width and height of each single collage picture according to border margin and bottom margin
        collage_picture_width = int(self.width - 2 * self.margin_width)
        collage_picture_height = int(self.height - 2 * self.margin_height - self.margin_bottom)

        collage_list = self._create_collage_list(1, collage_picture_width, collage_picture_height)

        self.collage_picture.paste(self.background)

        # take background image and paste each collage image on top of it with correct margin
        self.collage_picture.paste(collage_list[0], (self.margin_width, self.margin_height))  # top left

        if self.foreground is not None:
            self.collage_picture.paste(self.foreground, mask=self.foreground)

    def show_collage(self):
        self.collage_picture.show()

    def save_collage(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.collage_picture = self.collage_picture.convert('RGB')
        self.collage_picture.save(file_path, quality=95)
