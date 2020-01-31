import sys
from math import ceil
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QListView, QApplication, QStyledItemDelegate

from src.util import GetResourcePath, LoadColorDescriptions, CenterOnScreen, COLOR_DESCRIPTIONS_TYPE

_COLOR_FILE_PATH = 'colors.txt'
_WIDTH, _HEIGHT, _ITEM_SIZE, _SPACING = 500, 600, 50, 5


class App(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Color Description Viewer")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setGeometry(-1, -1, _WIDTH, _HEIGHT) # left, top, width, height
        CenterOnScreen(self)
        self._initUi()
        self.show()

    def _initUi(self):
        content = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(content)
        layout.setContentsMargins(10,10,0,10)
        self.setStyleSheet("background: white;")

        descriptions = LoadColorDescriptions(_COLOR_FILE_PATH)
        ColorViewer(descriptions, content)


class ColorViewer(QListView):
    def __init__(self, descriptions: COLOR_DESCRIPTIONS_TYPE, *args, **kwargs):
        super(ColorViewer, self).__init__(*args, **kwargs)
        self.setItemDelegate(ColorViewerItem(self))
        self.setEditTriggers(self.NoEditTriggers)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setFrameShape(self.NoFrame)
        self._model = QStandardItemModel(self)
        self.setModel(self._model)
        self.setSpacing(_SPACING)
        self._addColors(descriptions)
        self.setStyleSheet("ColorViewer { min-width: %spx; min-height: %spx; }" % (_WIDTH, _HEIGHT - 10))

    def _addColors(self, descriptions: COLOR_DESCRIPTIONS_TYPE):
        for i, color in enumerate(descriptions):
            alt = color.description_alt
            text = "%s: %s" % (i + 1, color)
            self._addColor(color.hex, text)

    def _addColor(self, color, description):
        item = QStandardItem('')
        item.setData(QColor(color))
        item.setSizeHint(QSize(_ITEM_SIZE, _ITEM_SIZE))
        item.setToolTip(description)
        self._model.appendRow(item)


class ColorViewerItem(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item = index.model().itemFromIndex(index)
        color = item.data()
        rect = option.rect
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRoundedRect(rect, 5, 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())