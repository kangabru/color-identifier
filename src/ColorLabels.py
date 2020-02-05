from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QIcon, QMouseEvent
from src.util import ColorDescription, GetClosestColor, COLOR_DESCRIPTIONS_TYPE, CopyToClipboard, GetResourcePath
from typing import List, Optional, Callable

_ICON_SIZE = 20


class ColorLabels(QWidget):
    _color = None

    def __init__(self, descriptions: COLOR_DESCRIPTIONS_TYPE):
        super().__init__()
        self._color_hex_code = _ColorHexCode()
        self._color_description = _ColorDescription(descriptions)
        copy_icon = _CopyIcon(self.copyColor)

        layout = QVBoxLayout(self)

        content = QWidget(self)
        color_layout = QHBoxLayout(content)
        color_layout.setContentsMargins(0,0,0,0)
        color_layout.addWidget(self._color_hex_code)
        color_layout.addWidget(copy_icon)

        layout.addWidget(content)
        layout.addWidget(self._color_description)

    def updateMessage(self, color: str):
        color = QColor(color)
        self._color = color
        self._color_hex_code.updateMessage(color)
        self._color_description.updateMessage(color)

    def copyColor(self):
        self._color and CopyToClipboard(self._color.name())


class _ColorHexCode(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("#------")
        self.setAlignment(Qt.AlignLeft)

    def updateMessage(self, color: QColor):
        self.setText(color.name())


class _ColorDescription(QLabel):
    def __init__(self, descriptions: COLOR_DESCRIPTIONS_TYPE):
        super().__init__()
        self.setText("-")
        self._descriptions = descriptions

    def updateMessage(self, color: QColor):
        color_description = GetClosestColor(color, self._descriptions)
        self.setText(color_description.description)


class _CopyIcon(QPushButton):
    def __init__(self, click_event: Callable):
        super().__init__()
        self._click_event = click_event
        self.setIconSize(QSize(_ICON_SIZE, _ICON_SIZE))
        self.setToolTip("Copy hex code to clipboard.")
        self.setIcon(QIcon(GetResourcePath("icon/copy.png")))
        self.setStyleSheet("border: none; border-radius: 0px;")

    def mousePressEvent(self, event: QMouseEvent):
        self._click_event()
        event.setAccepted(True) # Stop click event reaching the main window

    def mouseMoveEvent(self, event: QMouseEvent):
        event.setAccepted(True) # Stop drag event reacting on the main window