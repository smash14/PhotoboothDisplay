import os
import sys
import json
import tkinter.font
from tkinter import *
import logging
from PIL import Image, ImageTk, ImageOps
from utils import resource_path, is_windows, cleanup_printer_queue, get_gui_default_settings
import generate_settings
from collage.collage import Collage
from collage.connectPhotobooth import ConnectPhotobooth
from print_job_checker import print_job_checker
from generate_settings import generate_settings_main

if is_windows():
    from collage.printerCollage import PrinterCollage
else:
    from collage.printerCollageLinux import PrinterCollageLinux


# Global picture list with references to all photobooth pictures
picture_list = []

# Global variables to use with TKinter images
image_collage_2x2 = Image
image_collage_single = Image
img_printer = Image
pixel = Image
args = {}
gui_settings = {}


def update_picture_list():
    """
    Append Picture List with new pictures taken from photobox
    """
    global picture_list
    # TODO: Add proper error handling
    picture_list, new_image_added = photobooth.get_new_pictures()
    if new_image_added:
        return True
    return False


def open_settings_file():
    global args
    if not os.path.isfile('settings.json'):
        logging.warning("No settings file available, will create one for you...")
        generate_settings.generate_settings_main()
    with open('settings.json') as settings_file:
        file_contents = settings_file.read()
        logging.info("Found settings.json file")
    try:
        args = json.loads(file_contents)
    except Exception as e:
        logging.error(f"Error while reading settings.json file: {e}\r\n"
                      f"Please repair settings file manually or delete it!")
        raise SystemExit
    logging.info(json.dumps(args, indent=4))


def validating_args():
    # TODO: Add proper handling of height > width
    e = ""
    if args['collage_width'] < args['collage_height']:
        e = "Error: Collage target width must be smaller or equal than collage height."
    if args['collage_margin'] >= args['collage_height']:
        e = "Error: Collage margin must be smaller than collage height."
    if args['collage_margin'] >= args['collage_width']:
        e = "Error: Collage margin must be smaller than collage width."
    if args['collage_add_margin_bottom'] >= args['collage_height']:
        e = "Error: Collage additional margin bottom must be smaller than collage height."
    if args['collage_add_margin_bottom'] + args['collage_margin'] >= args['collage_height']:
        e = "Error: Collage margin plus additional margin bottom must be smaller than collage height."
    if type(args['printer_queue']) is not bool:
        e = f"Error: Entry 'printer_queue' must be 'true' or 'false', not {args['printer_queue']}"
    if not 'print_media_type' in args.keys():
        e = f"Error: Entry 'print_media_type' must be available in this version"
    if e:
        logging.error(e)
        raise Exception(e)

def open_and_validate_gui_settings():
    """
    Function to open and validate GUI settings
    """
    global gui_settings
    if not os.path.isfile('gui_settings.json'):
        logging.warning("No GUI settings file available, will create one for you...")
        with open('gui_settings.json', 'w') as outfile:
            default_gui_settings = get_gui_default_settings()
            json.dump(default_gui_settings, outfile, indent=4)
    with open('gui_settings.json') as gui_settings_file:
        file_contents = gui_settings_file.read()
        logging.info("Found gui_settings.json file")
    try:
        gui_settings.update(json.loads(file_contents))
    except Exception as e:
        logging.error(f"Error while reading gui_settings.json file: {e}\r\n"
                      f"Please repair settings file manually or delete it!")
        raise SystemExit
    logging.info(json.dumps(gui_settings, indent=4))

def list_printers():
    logging.info("You may use one of the following printer names:")
    if is_windows():
        printer_list = PrinterCollage()
    else:
        printer_list = PrinterCollageLinux()
    
    local_printers = printer_list.get_connected_printer()

    if is_windows():    
        for local_printer in local_printers:
            logging.info(local_printer[2])
    else:
        logging.info(local_printers)

    logging.info("---------------------------------")


def check_and_redraw_display():
    """
    Function to update TKinter GUI
    """
    global image_collage_2x2  # TODO Images of TKinter needs to be global to prevent garbage collector?!
    global image_collage_single
    global pixel

    # Popup to show printing process for a few seconds
    def open_popup():
        def _close_popup_after():
            if not print_job_checker(args['printer_name']) or args['printer_queue']:
                top.destroy()
            else:
                logging.info("Printer is still printing an image...")
                window.after(2000, _close_popup_after)

        global img_printer
        width = gui_settings['print_screen']['width']
        height = gui_settings['print_screen']['height']
        text = gui_settings['print_screen']['text']
        font = (gui_settings['print_screen']['font'], gui_settings['print_screen']['font_size'])
        img_printer = Image.open(resource_path(os.path.join("images", "print.jpg")))
        img_printer = ImageOps.fit(img_printer, (width, height))
        img_printer = ImageTk.PhotoImage(img_printer)
        top = Toplevel(window)
        top.title(text)
        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        top.geometry('%dx%d+%d+%d' % (width, height, x, y))
        top.overrideredirect(True)  # no window manager decorations
        Label(top, text=text, font=font).pack(pady=10)
        Label(top, image=img_printer).pack(pady=20)
        window.after(2000, _close_popup_after)
        window.update()

    def button_print_collage_2x2_clicked():
        def _enable_button_2x2_after():
            button_print_collage_2x2["state"] = "normal"

        logging.info("Button print collage 2x2 clicked")
        button_print_collage_2x2["state"] = "disable"
        if not print_job_checker(args['printer_name']) or args['printer_queue']:
            open_popup()
            printer.print_image(resource_path(os.path.join("images", "_collage2x2.jpg")))
        else:
            logging.warning("User requested printout, but there is still a photo in printer queue. Printout aborted")
        window.after(5000, _enable_button_2x2_after)

    def button_print_collage_1x1_clicked():
        def _enable_button_1x1_after():
            button_print_collage_1x1["state"] = "normal"

        logging.info("Button print collage 1x1 clicked")
        button_print_collage_1x1["state"] = "disable"
        if not print_job_checker(args['printer_name']) or args['printer_queue']:
            open_popup()
            printer.print_image(resource_path(os.path.join("images", "_collage1x1.jpg")))
        else:
            logging.warning("User requested printout, but there is still a photo in printer queue. Printout aborted")
        window.after(5000, _enable_button_1x1_after)

    if update_picture_list():
        # Create new 1x1 collage picture
        collage_1x1 = Collage(picture_list, args['collage_background'], args['collage_width'], args['collage_height'],
                              args['collage_margin'], args['collage_add_margin_bottom'],
                              args['collage_enhance_brightness'], args['collage_enhance_contrast'],
                              args['collage_foreground'])
        collage_1x1.create_collage_1x1()
        collage_1x1.save_collage(resource_path(os.path.join("images", "_collage1x1.jpg")))

        # Create new 2x2 collage picture
        collage_2x2 = Collage(picture_list, args['collage_background'], args['collage_width'], args['collage_height'],
                              args['collage_margin'], args['collage_add_margin_bottom'],
                              args['collage_enhance_brightness'], args['collage_enhance_contrast'],
                              args['collage_foreground'])
        collage_2x2.create_collage_2x2()
        collage_2x2.save_collage(resource_path(os.path.join("images", "_collage2x2.jpg")))

        # Get the current screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        padding_x = gui_settings['main_screen']['padding_x']
        padding_y = gui_settings['main_screen']['padding_y']
        picture_width = int(screen_width / 2 - padding_x * 2)
        button_width = int(picture_width)
        button_height = gui_settings['print_button']['height']

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
        label_collage_2x2.grid(row=0, column=0, padx=padding_x, pady=padding_y)

        # Create a Label Widget to display 1x1 Collage on right half of screen
        label_collage_single = Label(window, image=image_collage_single)
        label_collage_single.grid(row=0, column=1, padx=padding_x, pady=padding_y)

        # Create a Label Widget to display print buttons below each collage picture
        button_font = (gui_settings['print_button']['font'], gui_settings['print_button']['font_size'])
        print_button_text = gui_settings['print_button']['text']
        pixel = PhotoImage(width=1, height=1)  # create invisible image so width and height are interpreted as pixels
        button_print_collage_2x2 = Button(master=window, text=print_button_text, bg='#ffffff', image=pixel,
                                          width=button_width, height=button_height, compound="center",
                                          font=button_font, command=button_print_collage_2x2_clicked)
        button_print_collage_2x2.grid(row=1, column=0)

        button_print_collage_1x1 = Button(master=window, text=print_button_text, bg='#ffffff', image=pixel,
                                          width=button_width, height=button_height, compound="center",
                                          font=button_font, command=button_print_collage_1x1_clicked)
        button_print_collage_1x1.grid(row=1, column=1)

    # check for new pictures every 2 seconds
    window.after(args['photobooth_update_interval'], check_and_redraw_display)
    window.update()


if __name__ == '__main__':
    logging.basicConfig(filename='logfile.log', filemode='a', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("============================ V2.1.0 ============================")
    logging.info("Start Main Application")

    open_settings_file()
    validating_args()
    open_and_validate_gui_settings()
    list_printers()
    cleanup_printer_queue()

    window = Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", lambda event: window.quit())
    # put image in a label and place label as background
    wallpaper = Image.open(resource_path(os.path.join("images", "wallpaper.jpg")))
    wallpaper = ImageOps.fit(wallpaper, (window.winfo_screenwidth(),  window.winfo_screenheight()))
    wallpaper = ImageTk.PhotoImage(wallpaper)
    label_wp = Label(window, image=wallpaper)
    label_wp.place(x=0, y=0, relwidth=1, relheight=1)  # make label l to fit the parent window always

    # For testing purposes, a XAMPP instance can be used to simulate a connection to a Photobox
    # Use "createPicture.exe" located in the bin folder to create new pictures.
    photobooth = ConnectPhotobooth(args['photobooth_ssid'], args['photobooth_url'], args['photobooth_image_hash'])
    if is_windows():
        printer = PrinterCollage(args['printer_name'])
    else:
        printer = PrinterCollageLinux(args['printer_name'], args['print_media_type'], print_borderless=True )
    check_and_redraw_display()
    window.mainloop()
