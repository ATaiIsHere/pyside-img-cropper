import PySide6
from PySide6.QtCore import QPoint, Signal, QRect
from PySide6.QtGui import QColor, QPixmap, QMouseEvent, QPainter
from PySide6.QtWidgets import QLabel


class ImgBrowser(QLabel):
    mouseMoved = Signal(QPoint, QColor, QPixmap, QPoint, QPoint)

    def __init__(self, *args):
        super().__init__(*args)
        self._last_mouse_event = None
        self._viewable_range = 21
        self._source_pixmap: QPixmap | None = None
        self._selected_p1 = None
        self._selected_p2 = None
        self._selected_rect = None
        self.setMouseTracking(True)

    def set_viewable_range(self, viewable_range: int):
        self._viewable_range = viewable_range

    def viewable_range(self):
        return self._viewable_range

    def set_source_pixmap(self, pixmap):
        self._source_pixmap = pixmap
        self.setPixmap(self._source_pixmap)

    def cursor_safari(self):
        point = self._last_mouse_event.position().toPoint()
        (x, y) = point.toTuple()
        color = self.pixmap().toImage().pixelColor(x, y)
        rect = QRect(0, 0, self._viewable_range, self._viewable_range)
        rect.moveCenter(point)
        part = self.pixmap().copy(rect)
        self._last_mouse_event.scenePosition()
        return point, color, part, part.rect().center(), self._last_mouse_event.scenePosition().toPoint()

    def update_selected_rect(self):
        self._selected_rect = QRect(self._selected_p1, self._selected_p2)
        return self._selected_rect

    def get_selected_pixmap(self):
        return self._source_pixmap.copy(self._selected_rect) \
            if self._source_pixmap is not None and self._selected_rect is not None else None

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        self._selected_p2 = ev.position().toPoint()
        if self._source_pixmap is not None and self._selected_p1 is not None:
            print(self._selected_p1, self._selected_p2)
            pixmap = QPixmap(self._source_pixmap)
            p = QPainter(pixmap)
            p.drawRect(self.update_selected_rect())
            p.end()
            self.setPixmap(pixmap)

        self._last_mouse_event = ev
        self.mouseMoved.emit(*self.cursor_safari())

    def mousePressEvent(self, ev: PySide6.QtGui.QMouseEvent) -> None:
        self._selected_p1 = ev.position().toPoint()

    def mouseReleaseEvent(self, ev: PySide6.QtGui.QMouseEvent) -> None:
        if ev.position().toPoint() == self._selected_p1:
            self.setPixmap(self._source_pixmap)
        self._selected_p1 = None
