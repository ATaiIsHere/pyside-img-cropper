import numpy as np
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QGridLayout
from typing import List


class PixBrowser(QFrame):
    def __init__(self, *args):
        super().__init__(*args)
        self._grid_n = 21
        self._grid_list: List[List[QFrame | None]] | None = None
        self._grid_width = 0
        self._grid_style_sheet = ".QFrame#center { color: red; }"
        self._center_grid: QFrame | None = None
        self._center_width = 2

        self.setFrameStyle(1)
        self.setLineWidth(2)
        self.setMidLineWidth(1)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.build_grid_list()

    def build_grid(self, w, h):
        frame = self.reset_grid(QFrame())
        self.layout.addWidget(frame, w, h)
        return frame

    def reset_grid(self, frame: QFrame):
        frame.setObjectName("")
        frame.setFrameStyle(1)
        frame.setLineWidth(self._grid_width)
        frame.setStyleSheet(self._grid_style_sheet)
        return frame

    def set_center_grid(self, w, h):
        if self._center_grid is not None:
            self.reset_grid(self._center_grid)
        self._center_grid = self._grid_list[w][h]
        self._center_grid.setObjectName('center')
        self._center_grid.setLineWidth(self._center_width)

    def reset_grid_list(self):
        [self._grid_list[j][i].deleteLater() for j in range(len(self._grid_list)) for i in
         range(len(self._grid_list[j]))]

    def build_grid_list(self):
        if self._grid_list is not None:
            self.reset_grid_list()
        self._grid_list = [[self.build_grid(w, h) for w in range(self._grid_n)] for h in range(self._grid_n)]
        self.set_center_grid(self._grid_n // 2, self._grid_n // 2)

    def set_pixmap(self, pixmap: QPixmap):
        image = pixmap.toImage()
        (w, h) = image.size().toTuple()
        img_arr = np.array(image.bits()).reshape((h, w, 4))

        min_n = min(w, h)

        if min_n != self._grid_n:
            self._grid_n = min_n
            self.build_grid_list()

        def render_pos(w, h):
            (b, g, r, _) = img_arr[h][w]
            self._grid_list[w][h].setStyleSheet(f"""
                            {self._grid_style_sheet}
                            .QFrame {{ background-color: rgb{(r, g, b)} }}
                            """)

        [render_pos(i, j) for i in range(min_n) for j in range(min_n)]
