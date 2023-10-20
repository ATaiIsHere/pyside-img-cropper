from PySide6.QtWidgets import QWidget, QApplication, QLabel, QScrollArea, QFrame, QGridLayout, QStyle
from PySide6.QtCore import QRect, Qt, QSize, Signal, QPointF, Slot, QPoint, QEvent
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QColor
import PySide6
import numpy as np
import sys
from typing import List
from pix_browser import PixBrowser


class ImgContainer(QLabel):
    mouseMoved = Signal(QPoint, QColor, QPixmap)

    def __init__(self, *args):
        super().__init__(*args)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # print(ev)
        point = ev.position().toPoint()
        (x, y) = point.toTuple()
        color = self.pixmap().toImage().pixelColor(x, y)
        part = self.pixmap().copy(x - 7, y - 7, 11, 11)
        self.mouseMoved.emit(point, color, part)


class ImgMagnifier(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = self
        self.resize(1000, 500)

        self.label2 = ImgContainer('test2', self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setStyleSheet('background-color: #888888')
        self.label2.setPixmap(QPixmap(r'D:\ATai\Pictures\top_bg.jpg'))
        self.label2.setMouseTracking(True)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setMinimumSize(QSize(500, 500))
        self.scroll_area.setWidget(self.label2)

        self.label = QLabel('Position', self)
        self.label.setGeometry(600, 30, 650, 25)
        self.label2.mouseMoved.connect(self.update_label)

        self.label1 = QLabel('Position', self)
        self.label1.setGeometry(600, 60, 200, 200)

        self.frame = PixBrowser(self)
        self.frame.setGeometry(600, 260, 150, 150)
        self.frame.setStyleSheet('background-color: rgb(210,210,210)')

    @Slot()
    def update_label(self, point: QPoint, color: QColor, part: QPixmap):
        self.label.setText(f'{point.toTuple()} {color.getRgb()}')
        self.label1.setPixmap(part)
        self.frame.set_pixmap(part)

    # def event(self, event: PySide6.QtCore.QEvent) -> bool:
    #     print('test', event.type())
    #     print(2, event)
    #
    #     return QWidget.event(self, event)
    #
    # def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
    #     print(watched, event)
    #     if watched == self.scroll_area and event.type() == QEvent.Type.KeyPress:
    #         return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ImgMagnifier().show()

    sys.exit(app.exec())
