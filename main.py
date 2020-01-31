import sys
from os.path import exists
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QColor, QIcon, QMouseEvent
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QApplication

from src.ColorCircle import ColorCircle
from src.ColorPicker import getAverageColor, ScaleWindow
from src.ColorLabels import ColorLabels
from src.styles import Stylesheet
from src.util import GetResourcePath, LoadColorDescriptions, CenterOnScreen

_COLOR_FILE_PATH = 'colors.txt'
_SLOW_FACTOR = 0.3

class App(QDialog):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Color Identifier")
        self.setGeometry(-1, -1, 150, 50) # left, top, width, height
        self.setWindowIcon(QIcon(GetResourcePath("icon/icon.png")))

        CenterOnScreen(self)
        self.setStyleSheet(Stylesheet)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._initUi()
        self._initSignals()
        self.show()

        # Init the little zoom window
        self._viewer: QWidget = ScaleWindow()
        self._viewer_pos = None
        self._mouse_pos_slow = None

    def _initUi(self):
        content = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(content)

        hlayout = QHBoxLayout(content)
        hlayout.setContentsMargins(0,0,0,0)

        self.color_circle = ColorCircle()
        hlayout.addWidget(self.color_circle)

        descriptions = LoadColorDescriptions(self._get_color_file())
        self.color_labels = ColorLabels(descriptions)
        hlayout.addWidget(self.color_labels)

    def _get_color_file(self):
        """Returns the local color file if it exists, otherwise it uses the embedded color file."""
        return _COLOR_FILE_PATH if exists(_COLOR_FILE_PATH) else GetResourcePath(_COLOR_FILE_PATH)

    def _get_color_shades_file(self):
        return GetResourcePath(_COLOR_SHADES_FILE_PATH)

    def _initSignals(self):
        self._connectColorUpdates(self.colorChanged.connect)

    def _connectColorUpdates(self, func):
        func(self.color_circle.updateColor)
        func(self.color_labels.updateMessage)

    def mousePressEvent(self, event: QMouseEvent):
        self.setCursor(Qt.CrossCursor)
        self._viewer.show()
        self._viewer_pos = event.globalPos()
        self._mouse_pos_slow = event.globalPos()
        self._viewer_mods = event.modifiers()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.ArrowCursor)
        self._viewer.hide()

    def mouseMoveEvent(self, event: QMouseEvent):
        mouse_pos = event.globalPos()
        is_pressed_ctrl = event.modifiers() & Qt.ControlModifier

        # Global coordinates of where to sample the color
        sample_x, sample_y = mouse_pos.x(), mouse_pos.y()

        # Slow vs normal mode
        if is_pressed_ctrl:
            if self._mouse_pos_slow is None:
                self._mouse_pos_slow = mouse_pos # Init the point when slow mode was selected

            sample_pos = self._getSlowPoint(mouse_pos, self._mouse_pos_slow, is_pressed_ctrl)
            sample_x, sample_y = sample_pos.x(), sample_pos.y()
        else:
            self._mouse_pos_slow = None # Reset on ctrl release

        image, color = getAverageColor(sample_x, sample_y)
        self.colorChanged.emit(color)
        self._viewer.updateImage(mouse_pos, image.scaled(130, 130))
        self._viewer_mods = event.modifiers()

    def _getSlowPoint(self, mouse_pos: QPoint, slow_pos: QPoint, is_pressed_ctrl: bool):
        d_fact = _SLOW_FACTOR if is_pressed_ctrl else 1

        # Move the viewer position the full amount,
        d_pos = mouse_pos - slow_pos
        d_x, d_y = d_pos.x() * d_fact, d_pos.y() * d_fact
        return slow_pos + QPoint(d_x, d_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())