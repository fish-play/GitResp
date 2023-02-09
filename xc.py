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
        self.num = 0

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
        self.l4.setStyleSheet("background-color:rgb(245,245,245)")
        self.l4.resize(self.width() - 100, self.height() - self.l.height())
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.l4)

        self.l5 = QLabel(self)
        self.l5.setStyleSheet("background-color:yellow")

        # # 右侧小箭头
        self.stretch = QPushButton(self)
        self.stretch.setStyleSheet("background-color:rgb(0,150,0)")
        self.stretch.resize(20, 100)
        self.stretch.clicked.connect(self.clickButton)
        self.rpa = [qwer.Interior(self.l4) for i in range(10)]
        [self.rpa[i].move(13, 100 * i + 13) for i in range(len(self.rpa))]

    def clickButton(self):
        sender = self.sender()
        if self.is_move == True:
            print(sender.text() + '点击关闭')
            # self.l 最上层布局
            self.l.resize(self.width(), 50)
            # self.l2 最上层右侧布局
            self.l2.move(self.width() - self.l2.width(), 0)
            # self.l4 绿色层布局
            self.l4.resize(self.width(), 1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l4.move(0, self.l.height())
            # self.l5 隐藏层布局
            self.l5.resize(self.width() - self.l4.width(),
                           1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l5.move(self.l4.width(), self.l.height())
            # self.rpa 程序数据
            [self.rpa[i].resize(self.l4.width() - 80, 80) for i in range(len(self.rpa))]
            # self.stretch 隐藏开关布局
            self.stretch.move(self.width() - self.stretch.width(), self.height() / 2 - self.stretch.height())
            # self.scroll滚动条布局
            self.scroll.resize(self.l4.width() - self.stretch.width() - 5, self.height())
            self.scroll.move(0, self.l.height())
            self.is_move = False
        else:
            print(sender.text() + '点击打开')
            # self.l 最上层布局
            self.l.resize(self.width(), 50)
            # self.l2 最上层右侧布局
            self.l2.move(self.width() - self.l2.width(), 0)
            # self.l4 绿色层布局
            self.l4.resize(self.width() - 500, 1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l4.move(0, self.l.height())
            # self.l5 隐藏层布局
            self.l5.resize(self.width() - self.l4.width(),
                           1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l5.move(self.l4.width(), self.l.height())
            # self.rpa 程序数据
            [self.rpa[i].resize(self.l4.width() - 80, 80) for i in range(len(self.rpa))]
            # self.stretch 隐藏开关布局
            self.stretch.move(self.l4.width() - self.stretch.width(), self.height() / 2 - self.stretch.height())
            # self.scroll滚动条布局
            self.scroll.resize(self.l4.width() - self.stretch.width() - 5, self.height())
            self.scroll.move(0, self.l.height())
            self.is_move = True

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        print(self.is_move)
        if self.is_move is False:
            # self.l 最上层布局
            self.l.resize(self.width(), 50)
            # self.l2 最上层右侧布局
            self.l2.move(self.width() - self.l2.width(), 0)
            # self.l4 绿色层布局
            self.l4.resize(self.width(), 1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l4.move(0, self.l.height())
            # self.l5 隐藏层布局
            self.l5.resize(self.width() - self.l4.width(),
                           1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l5.move(self.l4.width(), self.l.height())
            # self.rpa 程序数据
            [self.rpa[i].resize(self.l4.width() - 80, 80) for i in range(len(self.rpa))]
            # self.stretch 隐藏开关布局
            self.stretch.move(self.l4.width() - self.stretch.width(), self.height() / 2 - self.stretch.height())
            # self.scroll滚动条布局
            self.scroll.resize(self.l4.width() - self.stretch.width() - 5, self.height())
            self.scroll.move(0, self.l.height())
        if self.is_move is True:
            # self.l 最上层布局
            self.l.resize(self.width(), 50)
            # self.l2 最上层右侧布局
            self.l2.move(self.width() - self.l2.width(), 0)
            # self.l4 绿色层布局
            self.l4.resize(self.width() - 500, 1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l4.move(0, self.l.height())
            # self.l5 隐藏层布局
            self.l5.resize(self.width() - self.l4.width(),
                           1200 if len(self.rpa) < 8 else 1200 + (len(self.rpa) - 8) * 200)
            self.l5.move(self.l4.width(), self.l.height())
            # self.rpa 程序数据
            [self.rpa[i].resize(self.l4.width() - 80, 80) for i in range(len(self.rpa))]
            # self.stretch 隐藏开关布局
            self.stretch.move(self.l4.width() - self.stretch.width(), self.height() / 2 - self.stretch.height())
            # self.scroll滚动条布局
            self.scroll.resize(self.l4.width() - self.stretch.width() - 5, self.height())
            self.scroll.move(0, self.l.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = TitleQWidget()
    a.show()
    sys.exit(app.exec_())
