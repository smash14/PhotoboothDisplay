import os
import sys
import subprocess
import requests
import shutil
import time
import hashlib
import logging

class ConnectPhotobooth:
    """
    Class to Connect with a Photobox WiFi Network
    """
    def __init__(self, ssid, image_url):
        """
        Parameters
        __________
        ssid : str
            SSID of Photbox WiFi network. Use "localhost" to mock for example a XAMPP instance
        image_url : str
            URL where to find the current picture in jpg format
        """
        self.ssid = ssid
        self.image_url = image_url

        self.picture_list = []

        self.tmp_pic_path = self.resource_path(os.path.join("tmp", "pic.jpg"))

        if not self._check_wlan_connection():
            e = f"Error: WiFi of Photobooth is not connected ({self.ssid})"
            logging.error(e)
            raise Exception(e)

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def _check_for_pyinstaller():
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        if getattr(sys, 'frozen', False):
            return True
        else:
            return False

    # function to establish a new connection
    def _check_wlan_connection(self, timeout=100):
        count = 0
        while count < timeout:
            wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
            data = wifi.decode('utf-8', 'ignore')
            if self.ssid in data:
                logging.info(f"Connection to WLAN {self.ssid} established!")
                self.connection_established = True
                return True
            elif self.ssid == "localhost":
                return True
            else:
                count = count + 1
                time.sleep(1)
        logging.error(f"Error: Could not connect to WiFi network: {self.ssid} after {timeout} seconds")
        return False

    def download_picture(self):
        """
        Download temporary image "pic.jpg" to "tmp/pic.jpg"
        :return:
        """
        if self._check_wlan_connection():
            try:
                r = requests.get(self.image_url, stream=True)
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    # Open a local file with wb ( write binary ) permission.
                    os.makedirs(os.path.dirname(self.tmp_pic_path), exist_ok=True)
                    with open(self.tmp_pic_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    logging.info(f"Image successfully downloaded: '{self.tmp_pic_path}'")
                    return True
                else:
                    logging.error('Image could not be retrieved')
                    return False
            except:
                logging.error(f"Failed to establish a new connection to {self.image_url}")
                return False

    def save_and_append_picture(self):
        """
        Check if temporary image is already in list of pictures. if not, copy new photo to "photo/CURR_TIME.jpg"
        append file path to picture_list
        :return:
        """
        try:
            curr_hash = self.calculate_hash(self.tmp_pic_path)
            if self.picture_list:
                prev_hash = self.calculate_hash(self.picture_list[-1])
            else:
                prev_hash = "000"
            if curr_hash != prev_hash:
                current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                target_filename = f"{current_time}.jpg"
                target_filepath = self.resource_path(os.path.join("photos", target_filename))
                os.makedirs(os.path.dirname(target_filepath), exist_ok=True)
                # Copy tmp image to photo folder
                shutil.copyfile(self.tmp_pic_path, target_filepath)
                if self._check_for_pyinstaller():
                    # also copy image outside of temp folder in case a PyInstaller instance is running
                    target_filepath = os.path.join("photos", target_filename)
                    os.makedirs(os.path.dirname(target_filepath), exist_ok=True)
                    shutil.copyfile(self.tmp_pic_path, target_filepath)
                    logging.info(f"App is running as executable, copy picture to '{target_filepath}'")
                self.picture_list.append(target_filepath)
                logging.info(f"Append picture list with image: '{target_filepath}', total list size: {len(self.picture_list)}")
                return True
            else:
                logging.info("Skip saving already existing image")
                return False
        except FileNotFoundError:
            logging.error("File not found")

    def get_picture_list(self):
        return self.picture_list

    def get_new_pictures(self):
        new_image_added = False
        error = True
        if self.download_picture():
            error = False
            if self.save_and_append_picture():
                new_image_added = True
        return self.picture_list, new_image_added, error

    @staticmethod
    def calculate_hash(file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
            hash_sum = hashlib.md5(data).hexdigest()
        return hash_sum
