""" 主窗口程序 """
import sys
from PyQt5.Qt import *
from lswj import xxxs as login_control
from qtpy import QtGui
import qwer


class TitleQWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._control()
        self.xxs = []
        # self.set_ui()

    def _control(self):
        self.is_move = False
        self.lo = QVBoxLayout()
        self.el = QHBoxLayout()
        self.l1 = QLabel()

    def set_ui(self):
        self.resize(1750,900)
        self.l1 = QLabel(self)
        self.l1.resize(self.width(), )
        self.l1.setStyleSheet("background-color:rgb(245,0,245);")

        self.l2 = QLabel(self)
        self.l2.resize(self.width()/2, 100)
        self.l2.setStyleSheet("background-color:rgb(0,0,245);")
        self.l2.move(0, 200)

        self.l3 = QLabel(self)
        self.l3.resize(self.width()/2, 100)
        self.l3.setStyleSheet("background-color:rgb(245,0,0);")
        self.l3.move(0,400)

        # self.lo.addWidget(self.l1)
        # self.el.addWidget(self.l2)
        # self.el.addWidget(self.l3)
        self.l1.setLayout(self.lo)



    def clickButton(self):

        ...

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
       ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = TitleQWidget()
    a.show()
    sys.exit(app.exec_())

