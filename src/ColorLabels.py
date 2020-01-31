from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from typing import List, Optional
from src.util import ColorDescription, GetClosestColor, COLOR_DESCRIPTIONS_TYPE


class ColorLabels(QWidget):
    def __init__(self, descriptions: COLOR_DESCRIPTIONS_TYPE):
        super().__init__()
        self._color_hex_code = _ColorHexCode()
        self._color_description = _ColorDescription(descriptions)

        layout = QVBoxLayout(self)
        layout.addWidget(self._color_hex_code)
        layout.addWidget(self._color_description)

    def updateMessage(self, *args):
        self._color_hex_code.updateMessage(*args)
        self._color_description.updateMessage(*args)


class _ColorHexCode(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("#------")

    def updateMessage(self, color):
        color = QColor(color)
        self.setText(color.name())


class _ColorDescription(QLabel):
    def __init__(self, descriptions: COLOR_DESCRIPTIONS_TYPE):
        super().__init__()
        self.setText("-")
        self._descriptions = descriptions

    def updateMessage(self, color: str):
        color = QColor(color)
        color_description = GetClosestColor(color, self._descriptions)
        self.setText(color_description.description)
