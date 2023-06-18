import os
import sys
from tkinter import *
from PIL import Image, ImageTk, ImageOps
from collage.collage import Collage
from collage.connectPhotobooth import ConnectPhotobooth
from collage.printerCollage import PrinterCollage
from utils import resource_path
import argparse
import logging

# Global picture list with references to all photobooth pictures
picture_list = []

# Global variables to use with TKinter images
image_collage_2x2 = Image
image_collage_single = Image
img_printer = Image

"""
Append Picture List with new pictures taken from photobox
"""
def update_picture_list():
    global picture_list
    picture_list, new_image_added = photobooth.get_new_pictures()
    if new_image_added:
        return True
    return False


def validating_args():
    # TODO: Add proper handling of height > width
    if args.collage_width < args.collage_height:
        e = "Error: Collage target width must be smaller or equal than collage height."
        logging.error(e)
        raise Exception(e)
    if args.collage_margin >= args.collage_height:
        e = "Error: Collage margin must be smaller than collage height."
        logging.error(e)
        raise Exception(e)
    if args.collage_margin >= args.collage_width:
        e = "Error: Collage margin must be smaller than collage width."
        logging.error(e)
        raise Exception(e)
    if args.collage_add_margin_bottom >= args.collage_height:
        e = "Error: Collage additional margin bottom must be smaller than collage height."
        logging.error(e)
        raise Exception(e)
    if args.collage_add_margin_bottom + args.collage_margin >= args.collage_height:
        e = "Error: Collage margin plus additional margin bottom must be smaller than collage height."
        logging.error(e)
        raise Exception(e)
    if args.list_printer:
        list_printers()


def list_printers():
    printer_list = PrinterCollage()
    local_printers = printer_list.get_connected_printer()
    logging.info("You may use one of the following printer names:\r\n")
    for local_printer in local_printers:
        logging.info(local_printer[2])
    print('\r\nPress any key to exit')
    x = input()
    quit()


"""
Function to update TKinter GUI
"""
def check_and_redraw_display():
    global image_collage_2x2  # TODO Images of TKinter needs to be global to prevent garbage collector?!
    global image_collage_single

    # Popup to show printing process for a few seconds
    def open_popup():
        global img_printer
        img_printer = Image.open(resource_path(os.path.join("images", "print.jpg")))
        img_printer = ImageOps.fit(img_printer, (800, 600))
        img_printer = ImageTk.PhotoImage(img_printer)
        top = Toplevel(window)
        top.title("Wird gedruckt...")
        # calculate position x and y coordinates
        width = 800
        height = 600
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        top.geometry('%dx%d+%d+%d' % (width, height, x, y))
        top.overrideredirect(True)  # no window manager decorations
        Label(top, text="Wird gedruckt...", font=('Helvetica 26 bold')).pack(pady=10)
        Label(top, image=img_printer).pack(pady=20)
        def close_after_2s():
            top.destroy()
        window.after(5000, close_after_2s)
        window.update()

    def button_print_collage_2x2_clicked():
        logging.info("Button print collage 2x2 clicked")
        printer.print_image(resource_path(os.path.join("images", "_collage2x2.jpg")))
        button_print_collage_2x2["state"] = "disable"
        open_popup()
        def enable_button_2x2_5s():
            button_print_collage_2x2["state"] = "normal"
        window.after(5000, enable_button_2x2_5s)

    def button_print_collage_1x1_clicked():
        logging.info("Button print collage 1x1 clicked")
        printer.print_image(resource_path(os.path.join("images", "_collage1x1.jpg")))
        button_print_collage_1x1["state"] = "disable"
        open_popup()
        def enable_button_1x1_5s():
            button_print_collage_1x1["state"] = "normal"
        window.after(5000, enable_button_1x1_5s)

    if update_picture_list():
        # Create new 1x1 collage picture
        collage_1x1 = Collage(picture_list, args.collage_background, args.collage_width, args.collage_height,
                              args.collage_margin, args.collage_add_margin_bottom)
        collage_1x1.create_collage_1x1()
        collage_1x1.save_collage(resource_path(os.path.join("images", "_collage1x1.jpg")))

        # Create new 2x2 collage picture
        collage_2x2 = Collage(picture_list, args.collage_background, args.collage_width, args.collage_height,
                              args.collage_margin, args.collage_add_margin_bottom)
        collage_2x2.create_collage_2x2()
        collage_2x2.save_collage(resource_path(os.path.join("images", "_collage2x2.jpg")))

        # Get the current screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        padding = 100
        picture_width = int(screen_width / 2 - padding * 2)

        # Create an object of tkinter ImageTk for Collage 2x2
        image_collage_2x2 = Image.open(resource_path(os.path.join("images", "_collage2x2.jpg")))
        wpercent = (picture_width / float(image_collage_2x2.size[0]))
        hsize = int((float(image_collage_2x2.size[1]) * float(wpercent)))
        image_collage_2x2 = image_collage_2x2.resize((picture_width, hsize), Image.LANCZOS)
        image_collage_2x2 = ImageTk.PhotoImage(image_collage_2x2)

        # Create an object of tkinter ImageTk for Collage 1x1
        image_collage_single = Image.open(resource_path(os.path.join("images", "_collage1x1.jpg")))
        wpercent = (picture_width / float(image_collage_single.size[0]))
        hsize = int((float(image_collage_single.size[1]) * float(wpercent)))
        image_collage_single = image_collage_single.resize((picture_width, hsize), Image.LANCZOS)
        image_collage_single = ImageTk.PhotoImage(image_collage_single)

        # Create a Label Widget to display 2x2 Collage on left half of screen
        label_collage_2x2 = Label(window, image=image_collage_2x2)
        label_collage_2x2.grid(row=0, column=0, padx=100, pady=100)

        # Create a Label Widget to display 1x1 Collage on right half of screen
        label_collage_single = Label(window, image=image_collage_single)
        label_collage_single.grid(row=0, column=1, padx=100, pady=100)

        # Create a Label Widget to display print buttons below each collage picture
        button_print_collage_2x2 = Button(master=window, text='Bild ausdrucken', width='100', height='5', bg='#CCCCCC',
                                          command=button_print_collage_2x2_clicked)
        button_print_collage_2x2.grid(row=1, column=0)

        button_print_collage_1x1 = Button(master=window, text='Bild ausdrucken', width='100', height='5', bg='#CCCCCC',
                                             command=button_print_collage_1x1_clicked)
        button_print_collage_1x1.grid(row=1, column=1)

    # check for new pictures every 2 seconds
    window.after(args.photobooth_update_interval, check_and_redraw_display)
    window.update()


if __name__ == '__main__':
    logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("====================================================================")
    logging.info("Start Main Application")

    # Init Arg Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-pssid", "--photobooth-ssid", type=str, default="localhost",
                        help="WiFi name of Photobooth. Windows must already know the SSID + password (default: %(default)s)")
    parser.add_argument("-purl", "--photobooth-url", type=str, default="http://127.0.0.1/photobooth/pic.jpg",
                        help="URL where to find the latest jpg (default: %(default)s)")
    parser.add_argument("-pui", "--photobooth-update_interval", type=int, default=2000,
                        help="Defines how often the photobooth URL will be checked for a new image in ms (default: %(default)s)")
    parser.add_argument("-cbg", "--collage-background", type=str, default="background.jpg",
                        help="Path to background image of collage picture (default: %(default)s)")
    parser.add_argument("-cw", "--collage-width", type=int, default=1800,
                        help="Width of final collage picture, should match printer paper (default: %(default)s)")
    parser.add_argument("-ch", "--collage-height", type=int, default=1200,
                        help="Height of final collage picture, should match printer paper (default: %(default)s)")
    parser.add_argument("-cm", "--collage-margin", type=int, default=5,
                        help="White border around each single picture within the collage (default: %(default)s)")
    parser.add_argument("-cmb", "--collage-add-margin-bottom", type=int, default=8,
                        help="Additional margin at the bottom of collage picture (default: %(default)s)")
    parser.add_argument("-pn", "--printer-name", type=str, default="Microsoft Print to PDF",
                        help="Name of the printer which should be used to print the collage picture (default: %(default)s)")
    parser.add_argument("-pl", "--list-printer", action="store_true",
                        help="Get the name of all available printers to use with --printer-name.")

    args = parser.parse_args()
    validating_args()

    window = Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", lambda event: window.quit())

    # For testing purposes, a XAMPP instance can be used to simulate a connection to a Photobox
    # Use "createPicture.exe" located in the bin folder to create new pictures.
    photobooth = ConnectPhotobooth(args.photobooth_ssid, args.photobooth_url)
    printer = PrinterCollage(args.printer_name)
    check_and_redraw_display()
    window.mainloop()
