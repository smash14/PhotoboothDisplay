import os
import sys
import logging
import subprocess


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def is_windows():
    """ Returns true if operating system is win32 type"""
    return sys.platform.startswith('win')

def cleanup_printer_queue():
    if not is_windows():
        print_command = ["cancel", '-a', '-x']
        try:
            result = subprocess.run(print_command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        except Exception as e:
            logging.error(f"Error while deleting pending print jobs: {e}")
            raise

        logging.info(f"Pending print jobs have been cancelled with return value: {result}")
        
        print_command = ["lpstat", '-o']
        try:
            result = subprocess.run(print_command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        except Exception as e:
            logging.error(f"Error while gathering pending print jobs: {e}")
            raise
        if result:
            logging.warning(f"It seems there are still pending print jobs after trying to cancel them: {result}")
        else:
            logging.info(f"No pending print jobs left {result}")
        return True

def get_gui_default_settings():
    gui_settings = {
        "main_screen": {
            "padding_x": 100,
            "padding_y": 50
        },
        "print_screen": {
            "width": 800,
            "height": 600,
            "text": "wird gedruckt...",
            "error_text": "Kein Papier",
            "font": "Helvetica 26 bold",
            "font_size": 26
        },
        "print_button": {
            "height": 100,
            "text": "Bild ausdrucken",
            "font": "Bahnschrift SemiBold SemiCondensed",
            "font_size": 24
        },
        "shutdown_message_box": {
            "title": "Herunterfahren",
            "message": "Möchten Sie den Drucker wirklich herunterfahren?",
            "size": 50,
            "placement_relx": 0.02,
            "placement_rely": 0.9
        }
    }
    return gui_settings

if __name__ == '__main__':
    cleanup_printer_queue()