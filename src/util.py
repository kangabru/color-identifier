import sys
from os import path
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from typing import List, Optional


def GetResourcePath(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.dirname(path.abspath(__file__)))) # Two dirs because we're inside a folder
    return path.join(base_path, relative_path)


class ColorDescription:
    hex: str = None
    color: QColor = None
    description: str = None
    description_alt: str = None

    def __init__(self, hex: str, description: str, description_alt: str = None):
        self.hex = hex
        self.color = QColor(hex)
        self.description = description
        self.description_alt = description_alt

    def __eq__(self, *args, **kargs):
        return self.hex.__eq__(*args, **kargs)

    def __hash__(self, *args, **kargs):
        return self.hex.__hash__(*args, **kargs)

    def __str__(self):
        h, d, a = self.hex, self.description, self.description_alt
        return "%s,%s,%s" % (h, d, a) if a else  "%s,%s" % (h, d)


COLOR_DESCRIPTIONS_TYPE = List[ColorDescription]

def LoadColorDescriptions(file_path: str) -> COLOR_DESCRIPTIONS_TYPE:
    descriptions = dict() # Insertion order is maintained from pyhton 3.6
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip().strip('\n')
            skip_line_message = "Skipping line #%s." % i
            if not line or line.startswith("//"): continue

            is_valid_line = line.startswith("#") and ',' in line
            if not is_valid_line:
                print(skip_line_message, "The line format should be like: #<Hex Code>,<Description>.")
                continue

            color, description, description_alt = None, None, None
            color, description = tuple(line.split(',', 1))
            if ',' in description:
                description, description_alt = tuple(description.split(',', 1))

            is_valid_color = QColor(color).isValid()
            if is_valid_color:
                # Don't set a value as we're just using the dict to maintain insertion order
                descriptions[ColorDescription(color, description, description_alt)] = None
            else:
                print(skip_line_message, "Color %s is not vlaid." % color)

    return descriptions.keys()


def GetClosestColor(color: QColor, descriptions: COLOR_DESCRIPTIONS_TYPE) -> Optional[ColorDescription]:
    r, g, b, _ = color.getRgb()

    min_diff_squared: int = None
    closest: ColorDescription = None

    for color_description in descriptions:
        _color = color_description.color

        _r, _g, _b, _ = _color.getRgb()
        diff_squared = (r - _r) ** 2 + (g - _g) ** 2 + (b - _b) ** 2

        if min_diff_squared is None or diff_squared < min_diff_squared:
            min_diff_squared = diff_squared
            closest = color_description

    return closest


def CenterOnScreen(widget: QWidget):
    resolution = QDesktopWidget().screenGeometry()
    widget.move((resolution.width() / 2) - (widget.frameSize().width() / 2),
                (resolution.height() / 2) - (widget.frameSize().height() / 2))