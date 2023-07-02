# Photobooth Collage Maker

Customizable Collage Maker for any kind of Photobooth.
Regularly checks for new jpg files at a given URL and automatically creates two collage images which are displayed on a fullscreen window. right side of the screen shows the latest single image and left side of the screen shows the latest 4 pictures in a 2 by 2 grid.
Below each picture is a print button located, which directly sends the collage picture to a defined printer.

Works with Windows only.

## Feature overview
![Screenshot 2022-04-27 175241](https://github.com/smash14/PhotoboothDisplay/assets/36343912/29ccfbbd-1c99-4518-b420-c056f1103d71)


- Regularly pulls a new jpg image from a given URL, time interval is adjustable
- Saves each new picture in a folder called "photos"
- Automatically creates two collage pictures with an adjustable border around each picture
- Supports to provide a background image for the collage pictures
- Directly print one of the collage pictures to a predefined printer
- Available as a single binary executable (PyInstaller)


## How to use
- Compile the script files on your own by using the provided requirements.txt file to install the required modules and the main.spec file to create your own executable.
- Or directly use the provided executable located in the bin folder

### Parameters
Use the following parameters:

| Parameter | Default Value                         | Description                                                                 | Note                                                                                   |
|-----------|---------------------------------------|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| -h        |                                       | Show help                                                                   |                                                                                        |
| -pssid    | localhost                             | WiFi Name of Photobooth                                                     | Initial connection to WiFi Network must be done using Windows to store Passcode        |
| -purl     | "http://127.0.0.1/photobooth/pic.jpg" | URL where to find the latest JPG image                                      |                                                                                        |
| -pui      | 2000                                  | Defines how often the photobooth URL will be checked for a new image in ms  |                                                                                        |
| --phash   | none                                  | URL of txt file which provides the md5 hash of the latest image             |                                                                                        |
| -cbg      | backgroung.jpd                        | Path to background image of collage picture                                 | Should match with parameter "width" and "height"                                       |
| -cw       | 1800                                  | Width of final collage picture                                              | should match printer paper                                                             |
| -ch       | 1200                                  | Height of final collage picture                                             | should match printer paper                                                             |
| -cm       | 5                                     | Transparent border around each single picture within the collage in percent |                                                                                        |
| -cmb      | 8                                     | Additional margin at the bottom of collage picture                          | Use this if you have for example a background image with additional text at the bottom |
| -ceb      | 1.0                                   | Factor to enhance brightness of collage picture                             | Only affects collage picture, not the original one                                     |
| -cec      | 1.0                                   | Factor to enhance contrast of collage picture                               | Only affects collage picture, not the original one                                     |
| -pn       | Microsoft Print to PDF                | Name of the printer which should be used to print the collage picture       | Use parameter -pl to receive a list of all available printers and their names          |
| -pl       |                                       | Get the name of all available printers to use with --printer-name.          |                                                                                        |
