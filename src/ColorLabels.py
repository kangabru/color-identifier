from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from typing import List, Optional
from src.util import ColorDescription, GetClosestColor

_DESCRIPTION_TYPE = List[ColorDescription]

class ColorLabels(QWidget):
    def __init__(self, descriptions: _DESCRIPTION_TYPE):
        super().__init__()
        self._color_hex_code = _ColorHexCode()
        self._color_description = _ColorDescription(descriptions)
        self._color_description_alt = _ColorDescriptionAlt(descriptions)

        layout = QVBoxLayout(self)
        layout.addWidget(self._color_hex_code)
        layout.addWidget(self._color_description)

        use_description_alt = sum([d.description_alt != None for d in descriptions])
        if use_description_alt:
            layout.addWidget(self._color_description_alt)

    def updateMessage(self, *args):
        self._color_hex_code.updateMessage(*args)
        self._color_description.updateMessage(*args)
        self._color_description_alt.updateMessage(*args)


class _ColorHexCode(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("#------")

    def updateMessage(self, color):
        color = QColor(color)
        self.setText(color.name())


class _ColorDescription(QLabel):
    def __init__(self, descriptions: _DESCRIPTION_TYPE):
        super().__init__()
        self.setText("-")
        self._descriptions = descriptions

    def updateMessage(self, color: str):
        color = QColor(color)
        color_description = GetClosestColor(color, self._descriptions)
        message = self._getMessage(color_description)
        self.setText(message)

    def _getMessage(self, description: Optional[ColorDescription]):
        return description.description if description else ""


class _ColorDescriptionAlt(_ColorDescription):
    def _getMessage(self, description: Optional[ColorDescription]):
        return description.description_alt if description else ""