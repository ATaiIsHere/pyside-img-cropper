from PySide6.QtWidgets import QWidget, QApplication, QLabel, QScrollArea, QFrame, QGridLayout, QStyle
from PySide6.QtCore import QRect, Qt, QSize, Signal, QPointF, Slot, QPoint, QEvent
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QColor, QCursor, QKeyEvent
import PySide6
import numpy as np
import sys
from typing import List
from pix_browser2 import PixBrowser


class ImgContainer(QLabel):
    mouseMoved = Signal(QPoint, QColor, QPixmap, QPoint)

    def __init__(self, *args):
        super().__init__(*args)
        self.PART_SIZE = 30

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        point = ev.position().toPoint()
        (x, y) = point.toTuple()
        color = self.pixmap().toImage().pixelColor(x, y)
        rect = QRect(0, 0, self.PART_SIZE, self.PART_SIZE)
        rect.moveCenter(point)
        part = self.pixmap().copy(rect)
        self.mouseMoved.emit(point, color, part, part.rect().center())


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
        self.scroll_area.installEventFilter(self)

        self.label = QLabel('Position', self)
        self.label.setGeometry(600, 30, 650, 25)
        self.label2.mouseMoved.connect(self.update_label)

        self.label1 = QLabel('Position', self)
        self.label1.setGeometry(600, 60, 200, 200)

        self.frame = PixBrowser(self.label2)
        self.frame.setGeometry(600, 260, 150, 150)
        self.frame.setStyleSheet('background-color: rgb(210,210,210)')

    @Slot()
    def update_label(self, point: QPoint, color: QColor, part: QPixmap, part_center: QPoint):
        self.label.setText(f'{point.toTuple()} {color.getRgb()} {part_center.toTuple()}')
        self.label1.setPixmap(part)
        self.frame.move(point + QPoint(50, 50))
        self.frame.set_pixmap(part, part_center)


    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        if watched == self.scroll_area and event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event)
            (x, y) = QCursor().pos().toTuple()
            if key_event.key() == Qt.Key.Key_Up:
                QCursor().setPos(x, y - 1)
                return True
            elif key_event.key() == Qt.Key.Key_Down:
                QCursor().setPos(x, y + 1)
                return True
            elif key_event.key() == Qt.Key.Key_Left:
                QCursor().setPos(x - 1, y)
                return True
            elif key_event.key() == Qt.Key.Key_Right:
                QCursor().setPos(x + 1, y)
                return True

        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = ImgMagnifier()
    a.show()

    sys.exit(app.exec())
