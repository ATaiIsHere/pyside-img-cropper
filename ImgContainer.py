import PySide6
from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor, Qt
from PySide6.QtWidgets import QScrollArea


class ImgContainer(QScrollArea):
    def __init__(self, *args):
        super().__init__(*args)

    def cursor_scroll(self, point: QPoint):
        (x, y) = point.toTuple()
        hb = self.horizontalScrollBar()
        vb = self.verticalScrollBar()
        if x < 50 and not hb.isMinimized():
            hb.setValue(hb.value() - 3)
        elif x > self.width() - 50 - vb.width() and not hb.isMaximized():
            hb.setValue(hb.value() + 3)
        if y < 50 and not vb.isMinimized():
            vb.setValue(vb.value() - 3)
        elif y > self.height() - 50 - hb.height() and not vb.isMaximized():
            vb.setValue(vb.value() + 3)

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