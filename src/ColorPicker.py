from PyQt5.QtCore import Qt, QRectF, QLineF
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget

_MARKER_SIZE = 100


def getAverageColor(x, y):
    window = int(QApplication.desktop().winId())
    image = QApplication.primaryScreen().grabWindow(window, x - 6, y - 6, 13, 13).toImage()
    color = image.pixelColor(6, 6)
    return image, color


class ScaleWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(ScaleWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(_MARKER_SIZE, _MARKER_SIZE)
        self.resize(1, 1)
        self.move(1, 1)
        self._image = None

    def updateImage(self, pos, image):
        self._image = image
        self.resize(image.size())
        self.move(pos.x() + 10, pos.y() + 10)
        self.show()
        self.update()

    def paintEvent(self, event):
        super(ScaleWindow, self).paintEvent(event)
        if self._image:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            path = QPainterPath()
            radius = min(self.width(), self.height()) / 2
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            painter.setClipPath(path)
            painter.drawImage(self.rect(), self._image)
            painter.setPen(QPen(QColor(0, 174, 255), 3))
            hw = self.width() / 2
            hh = self.height() / 2
            painter.drawLines(QLineF(hw, 0, hw, self.height()), QLineF(0, hh, self.width(), hh))
            painter.setPen(QPen(Qt.white, 3))
            painter.drawRoundedRect(self.rect(), radius, radius)