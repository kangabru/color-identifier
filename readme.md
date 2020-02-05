# ![Icon](https://raw.githubusercontent.com/kangabru/color-identifier/assets/assets/logo.png) Color Identifier

A simple desktop colour picker tool which helps you to identify colors by their color name.

Key Features:
- Pick colors anywhere on screen and the closest matching color name will be displayed.
- Includes a slow-mo mode for pixel accurate picking.
- Use the default colors or create your own! The app also ships with additional colors such as [CSS](https://www.w3schools.com/colors/colors_groups.asp), [xkcd](https://xkcd.com/color/rgb/), and even [Crayola](https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors) colors to help you get started.
- It's fast, and (should) support every OS and editing app like Photoshop or Lightroom.

![Banner Image](https://raw.githubusercontent.com/kangabru/color-identifier/assets/assets/banner.jpg)

---

## Usage

- Click inside the app and drag to analyse colours anywhere on screen.
- The hex code and color name will be displayed as the color changes.
- Hold down the `Ctrl` key to move slower in order to easily pick specific pixels.
- Use your own color names by following [this guide](colors/readme.md).

---

## Install

### (Optional) Setup Virtual Environment

`$ pip install virtualenv`

`$ virtualenv env`

Activate the environment via your IDE or manually with the scripts under `env/Scripts`.

### Install Packages

`$ pip install -r requirements.txt`

### Run Locally

`$ python main.py`

### Package Executable

`$ python package.py`

Note that [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/) is used to package the app. Adjustments may be required to package the app for non-windows operating systems.

---

## Technical Details

- The app is built with [Python](https://www.python.org/downloads/) and [Qt](https://pyqt5.com).
- Default color names were extracted from [this list of color shades](https://en.wikipedia.org/wiki/List_of_colors_by_shade).
- Further color names [can be found here](https://en.wikipedia.org/wiki/Lists_of_colors).

---

## Acknowledgments

- [This Qt widget repo](https://github.com/PyQt5/CustomWidgets) for the colour related widgets.