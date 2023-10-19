from PySide6.QtWidgets import QWidget, QApplication, QLabel, QScrollArea, QFrame, QGridLayout
from PySide6.QtCore import QRect, Qt, QSize, Signal, QPointF, Slot, QPoint
from PySide6.QtGui import QPixmap, QCursor, QMouseEvent, QColor
import numpy as np
import sys
from typing import List


class PixBrowser(QFrame):
    def __init__(self, n: int, *args):
        super().__init__(*args)
        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setMidLineWidth(1)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.frames_list: List[List[QFrame | None]] = [[None] * n for _ in range(n)]

        for h in range(n):
            for w in range(n):
                frame = QFrame()
                frame.setFrameStyle(1)
                frame.setLineWidth(1)
                self.frames_list[h][w] = frame
                layout.addWidget(frame, w, h)

        self.setLayout(layout)

    def set_pixmap(self, pixmap: QPixmap):
        image = pixmap.toImage()
        (w, h) = image.size().toTuple()
        img_arr = np.array(image.bits()).reshape((h, w, 4))

        for i in range(h):
            for j in range(w):
                (b, g, r, _) = img_arr[i][j]
                self.frames_list[i][j].setStyleSheet(f'background-color: rgb{(r, g, b)}')


class ImgContainer(QLabel):
    mouseMoved = Signal(QPoint, QColor, QPixmap)

    def __init__(self, *args):
        super().__init__(*args)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # print(ev)
        point = ev.position().toPoint()
        (x, y) = point.toTuple()
        color = self.pixmap().toImage().pixelColor(x, y)
        part = self.pixmap().copy(x - 7, y - 7, 15, 15)
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

        self.frame = PixBrowser(15, self)
        self.frame.setGeometry(600, 260, 150, 150)
        self.frame.setStyleSheet('background-color: rgb(210,210,210)')

    @Slot(QPointF)
    def update_label(self, point: QPoint, color: QColor, part: QPixmap):
        self.label.setText(f'{point.toTuple()} {color.getRgb()}')
        self.label1.setPixmap(part)
        self.frame.set_pixmap(part)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ImgMagnifier().show()

    sys.exit(app.exec())
