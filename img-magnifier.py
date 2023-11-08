from PySide6.QtWidgets import QWidget, QApplication, QLabel
from PySide6.QtCore import Qt, QSize, Slot, QPoint
from PySide6.QtGui import QPixmap, QColor
import PySide6
import sys

from ImgBrowser import ImgBrowser
from ImgContainer import ImgContainer
from PixBrowser2 import PixBrowser


class ImgMagnifier(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = self

        self.img_browser = ImgBrowser('', self)
        self.img_browser.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_browser.set_source_pixmap(QPixmap(r'D:\ATai\Pictures\top_bg.jpg'))
        self.img_browser.setMouseTracking(True)
        self.img_browser.mouseMoved.connect(self.update_label)

        self.scroll_area = ImgContainer(self)
        self.scroll_area.setMinimumSize(QSize(500, 500))
        self.scroll_area.setWidget(self.img_browser)

        self.label = QLabel('Position', self)
        self.label.setGeometry(600, 30, 650, 25)

        self.frame = PixBrowser(self)
        self.frame.setStyleSheet('background-color: rgb(210,210,210)')

    @Slot()
    def update_label(self, point: QPoint, color: QColor, part: QPixmap, part_center: QPoint, scene_pos: QPoint):
        self.frame.move(scene_pos + QPoint(50, 50))
        self.frame.set_pixmap(part, part_center)
        scroll_area_pos = scene_pos - self.scroll_area.pos()
        self.scroll_area.cursor_scroll(scroll_area_pos)

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.frame.move(event.pos() + QPoint(50, 50))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = ImgMagnifier()
    a.show()

    sys.exit(app.exec())
