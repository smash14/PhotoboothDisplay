import os
from tkinter import *
from PIL import Image, ImageTk, ImageOps
from collage.collage import Collage
from collage.connectPhotobooth import ConnectPhotobooth

picture_list = []
image_collage_4x4 = Image
image_collage_single = Image
image_printer = Image


def update_picture_list():
    global picture_list
    picture_list, new_image_added = photobooth.get_new_pictures()
    if new_image_added:
        return True
    return False


def check_and_redraw_display():
    global image_collage_4x4  # TODO Images of TKinter needs to be global to prevent garbage collector?!
    global image_collage_single

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

    def button_print_collage_4x4_clicked():
        print("Button print collage 4x4 clicked")
        button_print_collage_4x4["state"] = "disable"
        open_popup()
        def enable_button_5s():
            button_print_collage_4x4["state"] = "normal"
        window.after(5000, enable_button_5s)


    window.after(2000, check_and_redraw_display)
    if update_picture_list():
        collage_1x1 = Collage(picture_list)
        collage_1x1.create_collage_1x1()
        collage_1x1.save_collage("images/_collage1x1.jpg")

        collage_2x2 = Collage(picture_list)
        collage_2x2.create_collage_2x2()
        collage_2x2.save_collage("images/_collage4x4.jpg")

        # Get the current screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        padding = 100
        picture_width = int(screen_width / 2 - padding * 2)

        # Create an object of tkinter ImageTk for Collage 4x4
        image_collage_4x4 = Image.open("images/_collage4x4.jpg")
        wpercent = (picture_width / float(image_collage_4x4.size[0]))
        hsize = int((float(image_collage_4x4.size[1]) * float(wpercent)))
        image_collage_4x4 = image_collage_4x4.resize((picture_width, hsize), Image.LANCZOS)
        image_collage_4x4 = ImageTk.PhotoImage(image_collage_4x4)

        # Create an object of tkinter ImageTk for Collage 4x4
        image_collage_single = Image.open("images/_collage1x1.jpg")
        wpercent = (picture_width / float(image_collage_single.size[0]))
        hsize = int((float(image_collage_single.size[1]) * float(wpercent)))
        image_collage_single = image_collage_single.resize((picture_width, hsize), Image.LANCZOS)
        image_collage_single = ImageTk.PhotoImage(image_collage_single)

        # Create a Label Widget to display the text or Image
        label_collage_4x4 = Label(window, image=image_collage_4x4)
        label_collage_4x4.grid(row=0, column=0, padx=100, pady=100)

        label_collage_single = Label(window, image=image_collage_single)
        label_collage_single.grid(row=0, column=1, padx=100, pady=100)

        button_print_collage_4x4 = Button(master=window, text='+', width='100', height='5', bg='#00008B',
                                          command=button_print_collage_4x4_clicked)
        button_print_collage_4x4.grid(row=1, column=0)

        button_print_collage_single = Button(master=window, text='+', width='100', height='5', bg='#00008B',
                                             command=button_print_collage_single_clicked)
        button_print_collage_single.grid(row=1, column=1)
    window.update()

def button_print_collage_single_clicked():
    print("Button print collage single clicked")


if __name__ == '__main__':
    print("main")
    window = Tk()
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", lambda event: window.quit())

    photobooth = ConnectPhotobooth("localhost", "http://127.0.0.1/photobooth/pic.jpg")
    check_and_redraw_display()
    window.mainloop()
