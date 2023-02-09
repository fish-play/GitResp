# -*- coding=utf-8 -*-
""" 主窗口程序 """
import sys
from PyQt5.Qt import *
from qtpy import QtGui, QtCore


class Css(QObject):
    # css 编辑
    left_menu_label = "background-color: #F2F2F2;"


class StartWin(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._control()
        self.set_ui()

    def btu1(self):
        print("我被点击了")
        self.label2.setMinimumSize(260, self.height())

        self.label2.show()
        # 浮动窗口

        # dock_widget.setTitleBarWidget(QWidget())

    def set_ui(self):
        pass


    def _control(self):
        self.resize(1300,700)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)


        self.label1.setStyleSheet('background-color:red')
        self.label2.setStyleSheet('background-color:blue')


        self.label1.resize(self.width()-self.label2.width(), self.height())
        self.label1.move(160, 0)

        self.btu = QPushButton("展开",self.label1)


        dock_widget = QDockWidget("分组信息")
        dock_widget.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        dock_widget.setWidget(self.label2)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)
        dock_widget.setTitleBarWidget(QWidget())

        # 中心控件
        self.setCentralWidget(self.label1)

        self.btu.clicked.connect(self.btu1)

        self.label2.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = StartWin()
    a.show()
    sys.exit(app.exec_())

