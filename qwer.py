# -*- coding=utf-8 -*-
"""
1.如何监测for循环里的控件实时变动
2. 定位控件的相对位置
3.滚动条位置
"""
import random

""" 主窗口程序 """
import sys
from PyQt5.Qt import *
from qtpy import QtGui


class Interior(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_photo()

    def set_photo(self):
        self.resize(1000, 80)
        self.l = QLabel(self)
        self.l.setStyleSheet("background-color:rgb(197,246,249)")

        self.img = QLabel(self.l)
        self.img.setStyleSheet("background-color:rgb(6,72,251);;border-radius:8px ")

        self.text2 = QLabel(" 程序名称程序名称 ", self.l)
        self.text2.setFont(QFont("黑体", 10))
        self.text2.move(self.img.height() + 25, 16)

        self.text3 = QLabel(" 版本:1 ", self.l)
        self.text3.setFont(QFont("黑体", 8))
        self.text3.move(self.img.height() + 27, 50)

        self.text4 = QLabel(" 上次运行时间: 2022-10-24 12:00:00 ", self.l)
        self.text4.setFont(QFont("黑体", 8))
        self.text4.move(self.img.height() + 120, 50)

        self.img2 = QPushButton(self.l)
        self.img2.setStyleSheet("background-color:rgb(6,72,251);;border-radius:8px ")

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.l.resize(self.width(), 80)
        self.img.resize(self.l.height() / 2, self.l.height() / 2)
        self.img.move(13, self.l.height() / 2 - (self.l.height() / 2) / 2)
        self.img2.resize(self.l.height() / 2, self.l.height() / 2)
        self.img2.move(self.l.width() - 150, self.l.height() / 2 - (self.l.height() / 2) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Interior()
    a.show()
    sys.exit(app.exec_())
    # random.randint(7, 6)
