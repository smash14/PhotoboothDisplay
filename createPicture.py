import os
import shutil
import keyboard

# List of file names to iterate through
file_list = ['pic1.jpg', 'pic2.jpg', 'pic3.jpg', 'pic4.jpg', 'pic5.jpg', 'pic6.jpg']

# Current index in the file list
current_index = 0


def create_copy():
    global current_index

    # Remove the old "pic.jpg" file if it exists
    if os.path.exists('pic.jpg'):
        os.remove('pic.jpg')

    # Create a copy of the picture
    old_file_name = file_list[current_index]
    new_file_name = 'pic.jpg'
    shutil.copyfile(old_file_name, new_file_name)
    print(f'Created a copy of {old_file_name} as {new_file_name}.')

    # Increment the index or reset if it reaches the end of the list
    current_index = (current_index + 1) % len(file_list)


# Event handler for key press
def on_key_press(event):
    if event.name == 'enter':
        create_copy()


def main():
    # Hook the key press event
    keyboard.on_press(on_key_press)

    # Run the script indefinitely
    keyboard.wait()


if __name__ == '__main__':
    main()
