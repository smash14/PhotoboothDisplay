import sys
import time

from PIL import Image, ImageDraw, ImageFont
import os


def get_fonts(directory="fonts"):
    return [f for f in os.listdir(directory) if f.lower().endswith(".ttf")]


def get_backgrounds(directory="backgrounds"):
    return [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]


def choose_font(font_list):
    print("Choose a font:")
    for i, font_name in enumerate(font_list):
        print(f"{i + 1}. {font_name}")
    while True:
        try:
            choice = int(input("Enter font number: ")) - 1
            if 0 <= choice < len(font_list):
                return font_list[choice]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def choose_background(image_list):
    print("Available background images:")
    for i, name in enumerate(image_list):
        print(f"{i + 1}. {name}")
    while True:
        try:
            choice = int(input("Select background image number: ")) - 1
            if 0 <= choice < len(image_list):
                return image_list[choice]
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")


def main():
    # Step 1: Get user input
    print("v1.0")
    names = input("Enter names: ")
    date = input("Enter date: ")

    # Step 2: Load fonts
    font_dir = "fonts"
    fonts = get_fonts(font_dir)
    if not fonts:
        print("No ttf fonts found in 'fonts/' directory.")
        return
    selected_font = choose_font(fonts)
    font_path = os.path.join(font_dir, selected_font)

    # Load and choose background
    backgrounds = get_backgrounds("backgrounds")
    if not backgrounds:
        print("No background images found in 'backgrounds/' folder.")
        return

    selected_bg = choose_background(backgrounds)
    bg_path = os.path.join("backgrounds", selected_bg)

    # Load selected image
    try:
        img = Image.open(bg_path)
    except Exception as e:
        print(f"Failed to load image: {e}")
        return

    draw = ImageDraw.Draw(img)

    # Step 4: Load font
    font_size_input_names = input("Enter font size for names (default is 60): ").strip()
    font_size_names = int(font_size_input_names) if font_size_input_names.isdigit() else 60
    font_names = ImageFont.truetype(font_path, font_size_names)

    # Ask user for date font size (default = 35)
    date_font_size_input = input("Enter font size for date (default is 35): ").strip()
    date_font_size = int(date_font_size_input) if date_font_size_input.isdigit() else 35
    font_date = ImageFont.truetype(font_path, date_font_size)

    # Step 5: Draw text
    width, height = img.size

    # Positions
    # Ask user for margin with default value
    # Margins with defaults
    left_margin_input = input("Enter left margin (default is 110): ").strip()
    left_margin = int(left_margin_input) if left_margin_input.isdigit() else 110

    # right_margin_input = input("Enter right margin (default is 90): ").strip()
    right_margin = left_margin

    bottom_margin_input = input("Enter bottom margin (default is 80): ").strip()
    bottom_margin = int(bottom_margin_input) if bottom_margin_input.isdigit() else 80

    names_bbox = draw.textbbox((0, 0), names, font=font_names)
    date_bbox = draw.textbbox((0, 0), date, font=font_date)

    names_height = names_bbox[3] - names_bbox[1]
    date_width = date_bbox[2] - date_bbox[0]
    date_height = date_bbox[3] - date_bbox[1]

    names_position = (left_margin, height - names_height - bottom_margin)
    date_position = (width - date_width - right_margin, height - date_height - bottom_margin)

    draw.text(names_position, names, font=font_names, fill="white")
    draw.text(date_position, date, font=font_date, fill="white")

    # Step 6: Save image
    output_path = "background.jpg"
    img.save(output_path)
    print(f"Image saved as {output_path}")
    time.sleep(5)


if __name__ == "__main__":
    main()
