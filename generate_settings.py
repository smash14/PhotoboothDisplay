import argparse
import json
import os


def parse_args():
    # Init Arg Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-pssid", "--photobooth-ssid", type=str, default="localhost",
                        help="WiFi name of Photobooth. Windows must already know the SSID + password (default: %(default)s)")
    parser.add_argument("-purl", "--photobooth-url", type=str, default="http://127.0.0.1/photobooth/pic.jpg",
                        help="URL where to find the latest jpg (default: %(default)s)")
    parser.add_argument("-pui", "--photobooth-update_interval", type=int, default=2000,
                        help="Defines how often the photobooth URL will be checked for a new image in ms (default: %(default)s)")
    parser.add_argument("-phash", "--photobooth-image_hash", type=str, default=None,
                        help="URL of txt file which provides the md5 hash of the latest image (default: %(default)s)")
    parser.add_argument("-cbg", "--collage-background", type=str, default="background.jpg",
                        help="Path to background image of collage picture (default: %(default)s)")
    parser.add_argument("-cfg", "--collage-foreground", type=str, default=None,
                        help="Path to foreground image of collage picture (default: %(default)s)")
    parser.add_argument("-cw", "--collage-width", type=int, default=1800,
                        help="Width of final collage picture, should match printer paper (default: %(default)s)")
    parser.add_argument("-ch", "--collage-height", type=int, default=1200,
                        help="Height of final collage picture, should match printer paper (default: %(default)s)")
    parser.add_argument("-cm", "--collage-margin", type=int, default=5,
                        help="White border around each single picture within the collage (default: %(default)s)")
    parser.add_argument("-cmb", "--collage-add-margin-bottom", type=int, default=8,
                        help="Additional margin at the bottom of collage picture (default: %(default)s)")
    parser.add_argument("-ceb", "--collage-enhance_brightness", type=float, default=1.0,
                        help="Factor to enhance brightness of collage picture (default: %(default)s)")
    parser.add_argument("-cec", "--collage-enhance_contrast", type=float, default=1.0,
                        help="Factor to enhance contrast of collage picture (default: %(default)s)")
    parser.add_argument("-pn", "--printer-name", type=str, default="Microsoft Print to PDF",
                        help="Name of the printer which should be used to print the collage picture (default: %(default)s)")
    parser.add_argument("-pq", "--printer-queue", type=bool, default="False",
                        help="Allow a printer queue or wait until a picture has been fully printed by printer (default: %(default)s)")
    parser.add_argument("-pl", "--list-printer", action="store_true",
                        help="Get the name of all available printers to use with --printer-name.")

    return parser.parse_args()


def generate_settings_main():
    args = parse_args()
    with open("settings.json", "w", ) as outfile:
        json.dump(vars(args), outfile, indent=4)
    print(f"Settings file written to {os.path.abspath(outfile.name)}")
    print(json.dumps(vars(args), indent=4))


if __name__ == '__main__':
    generate_settings_main()
