# -*- coding=utf-8 -*-
import sys
from PyQt5.Qt import *
import settings


class LQLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("font-size:18px;border: 2px solid #c4c7ce;border-radius:5px;padding: 5px 0px;")


class LQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("font-size:18px")
        self.setAlignment(Qt.AlignBottom)


class ToolbarLQLabel(LQLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._control()
        self.set_ui()

    def _control(self):
        self.minimize_label = QLabel()
        self.close_label = QLabel()
        self.layout1 = QHBoxLayout()
        self.minimize_img = settings.IMAGES.get("minimize")
        self.close = settings.IMAGES.get("close")

    def set_ui(self):
        self.minimize_label.setPixmap(self.minimize_img)
        self.close_label.setPixmap(self.close_img)

        # 布局
        self.layout1.addWidget(self.minimize_label)
        self.layout1.addWidget(self.close)
        self.setLayout(self.layout1)
