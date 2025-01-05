# (C) http://timgolden.me.uk/python/win32_how_do_i/print.html

import os


import win32print
import win32ui
from PIL import Image, ImageWin
import logging

#
# Constants for GetDeviceCaps
#
#
# HORZRES / VERTRES = printable area
#
HORZRES = 8
VERTRES = 10
#
# LOGPIXELS = dots per inch
#
LOGPIXELSX = 88
LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111
#
# PHYSICALOFFSETX/Y = left / top margin
#
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113


class PrinterCollage:
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
        try:
            local_printer = win32print.EnumPrinters(2)
        except Exception as e:
            logging.error(f"Error while enumerating printers: {e}")
            raise
        return local_printer

    def _set_printer(self):
        local_printers = self.get_connected_printer()
        if self.printer_name.lower() == "default":
            self.selected_printer = win32print.GetDefaultPrinter()
            return True
        for local_printer in local_printers:
            if self.printer_name in local_printer:
                self.selected_printer = local_printer[2]
                return True
        return False

    def print_image(self, path_to_file):
        #
        # You can only write a Device-independent bitmap
        #  directly to a Windows device context; therefore
        #  we need (for ease) to use the Python Imaging
        #  Library to manipulate the image.
        #
        # Create a device context from a named printer
        #  and assess the printable size of the paper.
        #
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.selected_printer)
        printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
        # printer_size = (1200, 1800)  # for SELPHY CP1500: 4 x 6 inch with 300 dpi => 1200 x 1800

        if self.print_borderless:
            #  Force print borderless regardless of settings provided by the printer itself.
            #  NOTE: You may have to enable borderless printing in the Windows System Settings as well
            printable_area = printer_size
            printer_margins = (0, 0)
        else:
            printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
            printer_margins = hDC.GetDeviceCaps(PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

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
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate(90, expand=True)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        #
        # Start the print job, and draw the bitmap to
        #  the printer device at the scaled size.
        #
        hDC.StartDoc(path_to_file)
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
        logging.info(f"Image was sent to Printer: {self.selected_printer}")

        return True


if __name__ == '__main__':
    printer = PrinterCollage("Microsoft Print to PDF")
    printer.print_image("../images/_collage1x1.jpg")

