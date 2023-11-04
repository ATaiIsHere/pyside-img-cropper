import numpy as np
from PySide6.QtGui import QPixmap, QPainter, QResizeEvent, QPen, QColor
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel
from PySide6.QtCore import QRect, Qt, QPoint
from typing import List


class PixBrowser(QFrame):
    def __init__(self, *args):
        super().__init__(*args)
        self.BORDER_WIDTH = 8
        self.RATIO = 15
        self.label = QLabel(self)

        self.setFrameStyle(1)
        self.setLineWidth(self.BORDER_WIDTH)
        self.setMidLineWidth(1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        (w, h) = event.size().toTuple()
        self.label.resize(w - self.BORDER_WIDTH, h - self.BORDER_WIDTH)
        self.label.move(self.rect().center() - self.label.rect().center())

    def set_pixmap(self, pixmap: QPixmap, pixmap_center: QPoint):
        scaled_pixmap = pixmap.scaled(pixmap.size() * self.RATIO)
        self.resize(scaled_pixmap.size())

        p = QPainter(scaled_pixmap)
        pen = QPen()
        pen.setColor(QColor(255,0,0))
        p.setPen(pen)
        (cx, cy) = pixmap_center.toTuple()
        p.drawRect(QRect(cx * self.RATIO, cy * self.RATIO, self.RATIO, self.RATIO))
        p.end()
        self.label.setPixmap(scaled_pixmap)
