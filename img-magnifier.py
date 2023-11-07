from PySide6.QtWidgets import QWidget, QApplication, QLabel, QScrollArea, QFrame, QGridLayout, QStyle
from PySide6.QtCore import QRect, Qt, QSize, Signal, QPointF, Slot, QPoint, QEvent, QMargins
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QColor, QCursor, QKeyEvent
import PySide6
import numpy as np
import sys
from typing import List
from pix_browser2 import PixBrowser


class ImgBrowser(QLabel):
    mouseMoved = Signal(QPoint, QColor, QPixmap, QPoint, QPoint)
    mouseEntered = Signal()
    mouseLeft = Signal()

    def __init__(self, *args):
        super().__init__(*args)
        self._last_mouse_event = None
        self._viewable_range = 21
        self.setMouseTracking(True)

    def set_viewable_range(self, viewable_range: int):
        self._viewable_range = viewable_range

    def viewable_range(self):
        return self._viewable_range

    def cursor_safari(self):
        point = self._last_mouse_event.position().toPoint()
        (x, y) = point.toTuple()
        color = self.pixmap().toImage().pixelColor(x, y)
        rect = QRect(0, 0, self._viewable_range, self._viewable_range)
        rect.moveCenter(point)
        part = self.pixmap().copy(rect)
        self._last_mouse_event.scenePosition()
        return point, color, part, part.rect().center(), self._last_mouse_event.scenePosition().toPoint()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        self._last_mouse_event = ev
        self.mouseMoved.emit(*self.cursor_safari())

    def leaveEvent(self, event: PySide6.QtCore.QEvent) -> None:
        self.mouseLeft.emit()

    def enterEvent(self, event: PySide6.QtGui.QEnterEvent) -> None:
        self.mouseEntered.emit()


class ImgContainer(QScrollArea):
    def __init__(self, *args):
        super().__init__(*args)

    def cursor_scroll(self, point: QPoint):
        (x, y) = point.toTuple()
        hb = self.horizontalScrollBar()
        vb = self.verticalScrollBar()
        cursor = QCursor()
        if x < 50 and not hb.isMinimized():
            hb.setValue(hb.value() - 3)
            cursor.setPos(cursor.pos() + QPoint(3, 0))
        elif x > self.width() - 50 - vb.width() and not hb.isMaximized():
            hb.setValue(hb.value() + 3)
            cursor.setPos(cursor.pos() + QPoint(-3, 0))
        if y < 50 and not vb.isMinimized():
            vb.setValue(vb.value() - 3)
            cursor.setPos(cursor.pos() + QPoint(0, 3))
        elif y > self.height() - 50 - hb.height() and not vb.isMaximized():
            vb.setValue(vb.value() + 3)
            cursor.setPos(cursor.pos() + QPoint(0, -3))

    def keyPressEvent(self, key_event: PySide6.QtGui.QKeyEvent) -> None:
        (x, y) = QCursor().pos().toTuple()
        if key_event.key() == Qt.Key.Key_Up:
            QCursor().setPos(x, y - 1)
        elif key_event.key() == Qt.Key.Key_Down:
            QCursor().setPos(x, y + 1)
        elif key_event.key() == Qt.Key.Key_Left:
            QCursor().setPos(x - 1, y)
        elif key_event.key() == Qt.Key.Key_Right:
            QCursor().setPos(x + 1, y)


class ImgPanel(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.img_container = ImgContainer(self)
        # self.ima


class ImgMagnifier(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = self
        self.resize(1000, 500)

        self.img_browser = ImgBrowser('test2', self)
        self.img_browser.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_browser.setStyleSheet('background-color: #888888')
        self.img_browser.setPixmap(QPixmap(r'D:\ATai\Pictures\top_bg.jpg'))
        self.img_browser.setMouseTracking(True)
        self.img_browser.mouseMoved.connect(self.update_label)
        self.img_browser.mouseEntered.connect(self.turn_on_mouse_tracking)
        self.img_browser.installEventFilter(self)
        self.img_browser.mouseLeft.connect(self.turn_off_mouse_tracking)

        self.scroll_area = ImgContainer(self)
        self.scroll_area.setMinimumSize(QSize(500, 500))
        self.scroll_area.setWidget(self.img_browser)

        self.label = QLabel('Position', self)
        self.label.setGeometry(600, 30, 650, 25)

        self.label1 = QLabel('Position', self)
        self.label1.setGeometry(600, 60, 200, 200)

        self.frame = PixBrowser(self)
        self.frame.setStyleSheet('background-color: rgb(210,210,210)')

    @Slot()
    def update_label(self, point: QPoint, color: QColor, part: QPixmap, part_center: QPoint, scene_pos: QPoint):
        self.label.setText(f'{point.toTuple()} {color.getRgb()} {part_center.toTuple()}')
        self.label1.setPixmap(part)
        self.frame.move(scene_pos + QPoint(50, 50))
        self.frame.set_pixmap(part, part_center)
        scroll_area_pos = scene_pos - self.scroll_area.pos()
        self.scroll_area.cursor_scroll(scroll_area_pos)

    @Slot()
    def turn_on_mouse_tracking(self):
        self.setMouseTracking(True)

    @Slot()
    def turn_off_mouse_tracking(self):
        self.setMouseTracking(False)
        self.frame.resize(0, 0)

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        # print(event.pos().toTuple())
        self.frame.move(event.pos() + QPoint(50, 50))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = ImgMagnifier()
    a.show()

    sys.exit(app.exec())
