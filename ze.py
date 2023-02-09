# -*- coding=utf-8 -*-
"""
1.如何监测for循环里的控件实时变动
2. 定位控件的相对位置
3.滚动条位置
"""

""" 主窗口程序 """
import sys
from PyQt5.Qt import *
from lswj import xxxs as login_control
from qtpy import QtGui
import qwer

# class Interior(QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.set_photo()
#
#     def set_photo(self):
#         self.resize(1000, 80)




class TitleQWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._control()
        self.xxs = []
        self.set_ui()

    def _control(self):
        self.is_move = False
        self.lo = QVBoxLayout()

    def set_ui(self):
        self.resize(1580, 870)
        self.l = QLabel(self)
        self.l.setStyleSheet("background-color:rgb(245,245,245);")
        self.text1 = QLabel(" 我的程序 ", self.l)
        self.text1.setFont(QFont("黑体", 12))
        self.text1.move(10, 10)

        self.l.resize(self.width(), 50)

        self.l2 = QLabel(self.l)
        self.l2.setStyleSheet("background-color:rgb(245,245,245);")
        self.l2.resize(350, 50)

        self.l3 = QLabel(self.l2)
        self.l3.setStyleSheet("background-color:rgb(220,220,220);;border-radius:15px")
        self.l3.resize(200, 30)
        self.l3.move(0, 10)

        # 输入框
        self.search = QLineEdit(self.l3)
        self.search.setPlaceholderText("请输入程序名称搜索")
        self.search.setStyleSheet("border-radius:10px;")
        self.search.resize(140, 20)
        self.search.move(5, 5)

        # 放大镜
        self.grabble = QPushButton(self.l3)
        self.grabble.setStyleSheet("background-color:rgb(255,0,255);")
        self.grabble.resize(20, 20)
        self.grabble.move(170, 5)

        # 刷新
        self.refresh = QPushButton(self.l2)
        self.refresh.setStyleSheet("background-color:rgb(255,100,255);;border-radius:8px")
        self.refresh.resize(60, 30)
        self.refresh.move(230, 10)

        self.l4 = QLabel(self)
        self.l4.setStyleSheet("background-color:rgb(0,255,0)")
        self.l4.resize(self.width()-100, self.height() - self.l.height())

        # # 右侧小箭头
        self.stretch = QPushButton(self.l4)
        self.stretch.setStyleSheet("background-color:rgb(0,150,0)")
        self.stretch.resize(20, 100)

        self.rpa =[qwer.Interior(self.l4) for i in range(10)]
        [self.rpa[i].move(13, 100 * i + 13) for i in range(len(self.rpa))]


        # self.num = 10
        # e = 10
        # print(self.l4.height())

        # for i in range(self.num):

            # try:
            #     e += self.i.height() + 13
            #     print(self.i.height())
            # except:
            #     e = 13
            # self.variable(e)

            # ...
            # self.i = QLabel(self.l4)
            # self.i.setStyleSheet("background-color:rgb(197,246,249)")
            # self.i.resize(self.l4.width() - 200, self.l4.height() / self.num - 20)
            #
            # self.i.move(13, e)
            # e += self.i.height() + 13
            #
            # self.img = QLabel(self.i)
            # self.img.setStyleSheet("background-color:rgb(6,72,251);;border-radius:8px ")
            # self.img.resize(self.i.height() - 25, self.i.height() - 25)
            # self.img.move(13, self.i.height() / 2)
            # print(self.l4.height())
            # print(self.i.height())
            #
            # self.text2 = QLabel(" 程序名称程序名称 ", self.i)
            # self.text2.setFont(QFont("黑体", 10))
            # self.text2.move(self.img.height() + 16, 16)
            #
            # self.text3 = QLabel(" 版本:1 ", self.i)
            # self.text3.setFont(QFont("黑体", 8))
            # self.text3.move(self.img.height() + 18, 40)
            #
            # self.text4 = QLabel(" 上次运行时间: 2022-10-24 12:00:00 ", self.i)
            # self.text4.setFont(QFont("黑体", 8))
            # self.text4.move(self.img.height() + 120, 40)
            #
            # self.img2 = QPushButton(self.i)
            # self.img2.setStyleSheet("background-color:rgb(6,72,251);;border-radius:8px ")
            # self.img2.resize(self.i.height() - 25, self.i.height() - 25)
            # self.img2.move(self.i.width() - 120, self.i.height() / 2 - (self.i.height() - 25) / 2)
        #
        #     self.lo.addWidget(self.i)
        #
        # self.l4.setLayout(self.lo)

        # self.l5 = QLabel()
        # # self.l6 = QLabel()
        # # self.l7 = QLabel()
        # self.l5.setStyleSheet("background-color:rgb(0,0,0)")


        # self.l6.setStyleSheet("background-color:rgb(0,0,0)")
        # self.l7.setStyleSheet("background-color:rgb(0,0,0)")

        # self.lo.addWidget(self.l5)
        # self.lo.addWidget(self.l6)
        # self.lo.addWidget(self.l7)
        # self.l4.setLayout(self.lo).

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.l.resize(self.width(), 50)
        self.l2.move(self.width() - self.l2.width(), 0)
        self.l4.resize(self.width(), self.height() - self.l.height())
        self.l4.move(0, self.l.height())
        print(111)
        # [self.rpa[i].move(13, 100 * i + 13) for i in range(len(self.rpa))]
        [self.rpa[i].resize(self.l4.width()-200, 80) for i in range(len(self.rpa))]
        self.stretch.move(self.width() - self.stretch.width(), self.l4.height() / 2 - self.stretch.height())



if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # a = TitleQWidget()
    # a.show()
    # sys.exit(app.exec_())
    x = 1+(2 if 0 else -1)
    print(x)