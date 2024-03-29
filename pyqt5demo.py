from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QLineEdit
import os
import fitz
import time
import sys
from log import logger
import win32print
import win32api
import PyPDF2
from docx import Document
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

# printers = []
# for it in win32print.EnumPrinters(2):
#     printers.append(it[2])
    # print(printers)

class UiForm(object):
    def setupUi(self, Form):
        """
        设置打开文书路径的类
        """
        Form.setObjectName("Form")
        Form.resize(443, 120)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 40, 301, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openFileButton = QtWidgets.QPushButton(self.widget)
        self.openFileButton.setObjectName("openFileButton")
        self.horizontalLayout.addWidget(self.openFileButton)
        self.filePathlineEdit = QtWidgets.QLineEdit(self.widget)
        self.filePathlineEdit.setObjectName("filePathlineEdit")
        self.horizontalLayout.addWidget(self.filePathlineEdit)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "QFileDialog打开文件例子"))
        self.openFileButton.setText(_translate("Form", "打开文件"))


class InputdialogDemo(QWidget, UiForm):
    def __init__(self, parent=None):
        super(InputdialogDemo, self).__init__(parent)
        self.set_photo()
        self.setWindowTitle("PDF拆分")

    def set_photo(self):
        """
        配置控件大小，类型
        """
        self.resize(600, 200)
        self.l = QLabel(self)
        self.t = QFormLayout()
        # self.l.setStyleSheet("background-color:rgb(197,246,249)")
        self.l.setPixmap(QPixmap('./photo/img.png').scaled(self.width(), self.height()))
        # self.l.setStyleSheet(self.label)

        self.text1 = QPushButton("文书所在文件夹", self.l)
        self.text1.setFont(QFont("黑体", 10))
        self.text1.clicked.connect(self.openfile)
        self.le1 = QLineEdit()
        self.t.addRow(self.text1, self.le1)

        self.text2 = QPushButton("文书存放地址", self.l)
        self.text2.setFont(QFont("黑体", 10))
        self.text2.clicked.connect(self.openfile2)
        self.le2 = QLineEdit()
        self.t.addRow(self.text2, self.le2)

        self.text3 = QLabel("选择", self.l)
        self.text3.setFont(QFont("黑体", 10))
        # self.le3 = QComboBox()
        # for i in printers:
        #     self.le3.addItem(i)
        # self.t.addRow(self.text3, self.le3)

        self.button1 = QPushButton("运行", self.l)
        self.button1.setFont(QFont("黑体", 10))
        self.button1.setStyleSheet("background-color:pink")
        self.button1.clicked.connect(self.on_button_clicked)
        self.setLayout(self.t)

    def printer_loading(self, _dir_path, save_path, dyj_name, chooseDuplex=2, chooseColor=0, chooseCopies=1):

        """控制打印机"""
        for _ in os.listdir(_dir_path):

            f = os.path.join(_dir_path, _)
            handle = win32print.SetDefaultPrinter(dyj_name)
            printer = win32print.GetDefaultPrinter()
            PRINTER_DEFAULTS = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
            pHandle = win32print.OpenPrinter(printer, PRINTER_DEFAULTS)
            level = 2
            properties = win32print.GetPrinter(pHandle, level)
            pDevModeObj = properties["pDevMode"]
            pDevModeObj.Duplex = int(chooseDuplex)
            pDevModeObj.Orientation = 2
            pDevModeObj.Color = int(chooseColor)
            pDevModeObj.Copies = int(chooseCopies)
            properties["pDevMode"] = pDevModeObj
            try:
                win32print.SetPrinter(pHandle, level, properties, 0)
            except Exception as e:
                raise Exception(f"设置打印机出错了，\n错误原因：{e}")
            res = win32api.ShellExecute(0, 'print', f, None, '.', 0)
            time.sleep(2)
            win32print.ClosePrinter(pHandle)
            path = os.path.join(save_path, f"save.txt")
            with open(path, "a") as file:
                file.write(f"{f}\n")
            logger.info(f"{f}打印成功")

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """
        用于设置控件大小及位置
        """
        self.l.resize(self.width(), self.height())
        self.button1.resize(70, 40)
        self.button1.move(self.width() / 2, 110)

    def on_button_clicked(self):
        """
        用于获取输入框中的数据，调用执行脚本
        """
        # 获取文本框里的值
        file1 = self.le1.text()
        file2 = self.le2.text()
        # file3 = self.le3.currentText()
        print(file1)
        print(file2)
        # print(file3)
        self.pdf_docx(file1, file2)
        # self.pdf_split(file1, file2)
        # self.printer_loading(_dir_path=file1, save_path=file2, dyj_name=file3)

    def openfile(self):
        """
        设置选择文书路径
        """
        get_directory_path = QFileDialog.getExistingDirectory(self, "选取指定文件夹",
                                                              "C:/")
        self.le1.setText(str(get_directory_path))

    def openfile2(self):
        get_directory_path = QFileDialog.getExistingDirectory(self, "选取指定文件夹",
                                                              "C:/")
        self.le2.setText(str(get_directory_path))

    def pdf_docx(self, file1, file2):
        for i in os.listdir(file1):
            pdf_file = open(os.path.join(file1, i), "rb")
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            doc = Document()
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                doc.add_paragraph(text)
            name = i.replace(".pdf", ".docx")
            doc.save(os.path.join(file2, name))





    def pdf_split(self, file1, file2):
        """
        运行的拆分的主函数
        """
        seg_num = 1
        output_dir = file2
        for e in os.listdir(file1):
            if ".pdf" not in e:
                continue
            pdf_path = os.path.join(file1, e)
            pdf_doc = fitz.open(pdf_path)
            num_page = pdf_doc.page_count
            pages = [i for i in range(0, num_page, seg_num)]
            for i, pages_start in enumerate(pages):
                pages_end = pages_start + seg_num - 1
                dist_pdf = fitz.open()
                dist_pdf.insert_pdf(pdf_doc, from_page=pages_start, to_page=pages_end)
                pdf_name = os.path.basename(pdf_path)
                savepdf = os.path.join(output_dir, f'{i}.pdf')
                dist_pdf.save(savepdf)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = InputdialogDemo()
    demo.show()
    sys.exit(app.exec_())
