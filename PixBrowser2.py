import numpy as np
from PySide6.QtGui import QPixmap, QPainter, QResizeEvent, QPen, QColor
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel
from PySide6.QtCore import QRect, Qt, QPoint
from typing import List


class PixBrowser(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.SIZE_N = 200
        self.BORDER_WIDTH = 8
        self.RATIO = 15

    def set_pixmap(self, pixmap: QPixmap, pixmap_center: QPoint):
        self.setPixmap(pixmap)

        ratio = self.SIZE_N // max(*pixmap.size().toTuple())
        scaled_pixmap = pixmap.scaled(pixmap.size() * ratio)

        self.resize(ratio * max(*pixmap.size().toTuple()), ratio * max(*pixmap.size().toTuple()))

        p = QPainter(scaled_pixmap)
        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        p.setPen(pen)
        (cx, cy) = pixmap_center.toTuple()
        p.drawRect(QRect(cx * ratio, cy * ratio, ratio, ratio))

        pen = QPen()
        pen.setColor(QColor(0, 0, 0))
        pen.setWidth(self.BORDER_WIDTH * 2)
        p.setPen(pen)
        p.drawRect(scaled_pixmap.rect())
        p.end()
        self.setPixmap(scaled_pixmap)
