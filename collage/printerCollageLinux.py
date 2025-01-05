import os
from PIL import Image, ImageWin
import subprocess
import logging

class PrinterCollageLinux:
    def __init__(self, printer_name="default", print_borderless=True):
        self.printer_name = printer_name
        self.print_borderless = print_borderless

        self.selected_printer = ""
        if not self._set_printer():
            e = f"Error: Could not find any connected printer named ({self.printer_name})"
            logging.error(e)
            raise Exception(e)

    @staticmethod
    def get_connected_printer():
        """
        returns string of all connected printers.
        e.g. 'printer Brother_MFC_J5910DW is idle.  enabled since Sun 05 Jan 2025 08:53:34 CET\nprinter Canon_SELPHY_CP1500 is idle.  enabled since Sat 04 Jan 2025 21:07:06 CET\n'
        """
        try:
            connected_printer = subprocess.run(['lpstat', '-p'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        except Exception as e:
            logging.error(f"Error while enumerating printers: {e}")
            raise
        return connected_printer

    def _set_printer(self):
        local_printers = self.get_connected_printer()
        if self.printer_name == "default":
            return True
        if self.printer_name in local_printers:
            return True
        return False

    def print_image(self, path_to_file):
        #
        # Open the image, rotate it if it's wider than
        #  it is high, and work out how much to multiply
        #  each pixel by to get it as big as possible on
        #  the page without distorting.
        #
        try:
            bmp = Image.open(path_to_file)
            logging.info(f"open image for printing: {path_to_file}")
        except FileNotFoundError:
            logging.error(f"Error: Could not find image {path_to_file}")
            return False

        #
        # Start the print job using CUPS
        #  the printer device at the scaled size.
        #
        print_command = ["lp", '-d', self.printer_name, '-o', 'media=Postcard,StpiShrinkOutput=Expand,StpBorderless=True', path_to_file]

        try:
            result = subprocess.run(print_command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        except Exception as e:
            logging.error(f"Error while enumerating printers: {e}")
            raise

        logging.info(f"Image was sent to Printer: {self.selected_printer} with return: {result}")

        return True


if __name__ == '__main__':
    printer = PrinterCollageLinux("Brother_MFC_J5910DW")
    printer.print_image("bild.jpg")

