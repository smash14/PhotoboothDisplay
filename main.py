import os
from tkinter import *
from PIL import Image, ImageTk, ImageOps
from collage.collage import Collage
from collage.connectPhotobooth import ConnectPhotobooth

# Global picture list with references to all photobooth pictures
picture_list = []

# Global variables to use with TKinter images
image_collage_2x2 = Image
image_collage_single = Image
image_printer = Image

"""
Append Picture List with new pictures taken from photobox
"""
def update_picture_list():
    global picture_list
    picture_list, new_image_added = photobooth.get_new_pictures()
    if new_image_added:
        return True
    return False

"""
Functino to update TKinter GUI
"""
def check_and_redraw_display():
    global image_collage_2x2  # TODO Images of TKinter needs to be global to prevent garbage collector?!
    global image_collage_single

    # Popup to show printing process for a few seconds
    def open_popup():
        global img_printer
        img_printer = Image.open(os.path.join("images", "print.jpg"))
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
        window.after(2000, close_after_2s)
        window.update()

    def button_print_collage_2x2_clicked():
        print("Button print collage 4x4 clicked")
        button_print_collage_2x2["state"] = "disable"
        open_popup()
        def enable_button_5s():
            button_print_collage_2x2["state"] = "normal"
        window.after(5000, enable_button_5s)

    if update_picture_list():
        # Create new 1x1 collage picture
        collage_1x1 = Collage(picture_list)
        collage_1x1.create_collage_1x1()
        collage_1x1.save_collage("images/_collage1x1.jpg")

        # Create new 2x2 collage picture
        collage_2x2 = Collage(picture_list)
        collage_2x2.create_collage_2x2()
        collage_2x2.save_collage("images/_collage2x2.jpg")

        # Get the current screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        padding = 100
        picture_width = int(screen_width / 2 - padding * 2)

        # Create an object of tkinter ImageTk for Collage 2x2
        image_collage_2x2 = Image.open("images/_collage2x2.jpg")
        wpercent = (picture_width / float(image_collage_2x2.size[0]))
        hsize = int((float(image_collage_2x2.size[1]) * float(wpercent)))
        image_collage_2x2 = image_collage_2x2.resize((picture_width, hsize), Image.LANCZOS)
        image_collage_2x2 = ImageTk.PhotoImage(image_collage_2x2)

        # Create an object of tkinter ImageTk for Collage 1x1
        image_collage_single = Image.open("images/_collage1x1.jpg")
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

        button_print_collage_single = Button(master=window, text='Bild ausdrucken', width='100', height='5', bg='#CCCCCC',
                                             command=button_print_collage_1x1_clicked)
        button_print_collage_single.grid(row=1, column=1)

    # check for new pictures every 2 seconds
    window.after(2000, check_and_redraw_display)
    window.update()

def button_print_collage_1x1_clicked():
    print("Button print collage single clicked")


if __name__ == '__main__':
    print("main")
    window = Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", lambda event: window.quit())

    # For testing purposes, a XAMPP instance can be used to simulate a connection to a Photobox
    # Use "createPicture.exe" located in the bin folder to create new pictures.
    photobooth = ConnectPhotobooth("localhost", "http://127.0.0.1/photobooth/pic.jpg")  # TODO: Replace with actual URL of Photobooth
    check_and_redraw_display()
    window.mainloop()
