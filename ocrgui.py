#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import re
import sys
import warnings
import os
import time
from PIL import Image
import pickle
import pytesseract
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QProgressBar
from PyQt5.QtGui import QIcon, QPicture
from PyQt5.QtCore import *
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
warnings.filterwarnings("ignore")

cwd = os.path.dirname(os.path.abspath(__file__))
print (cwd)
dtout = ''
filename = "ocr.ui"
filename = f"{cwd}/{filename}"
Form, Base = uic.loadUiType(filename)

class MyWindow(QtWidgets.QWidget, Form):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Form()
        self.ui.setupUi(self)
        self.ui.btnQuit.clicked.connect(QCoreApplication.instance().quit)
        self.ui.btnQuit.setToolTip("Выход")
        self.ui.btnConv.setToolTip("Распознать")
        self.ui.showd.clicked.connect(self.getfiles)
        self.ui.btnSave.clicked.connect(self.save_f)
        self.ui.showd.setToolTip("Открывает изображение")
        self.ui.mylabel_2.setText("Входное изображение")
        self.ui.btnConv.clicked.connect(self.ocr)
        self.ui.mylabel.setText(f" ")
       
    def getfiles(self):
        global fname
        global fout
        with open(f"{cwd}/path.txt", 'r') as f_read:
            pth = f_read.read()
            print (f"{pth}")
        fname = QFileDialog.getOpenFileName(self, "Open PNG", f"{pth}/", "PNG (*.png);;GIF (*.gif);;JPG (*.jpg *.jpe *.JPEG );;TIFF (*.tiff);;All (*)")[0]
        if fname == '':
            QFileDialog(self, quit())
        with open(fname, 'rb') as data:
            self.ui.mylabel_2.setScaledContents(True)
            self.ui.mylabel.setText(f"Файл: {fname}")
            self.ui.mylabel_2.setPixmap(QtGui.QPixmap(f"{fname}"))
        print (f"\n{fname}")
        fout = re.sub(r'\.png|\.PNG', '', fname)
        dir_path = os.path.dirname(fname)
        with open(f"{cwd}/path.txt", 'w') as f_out:
            f_out.write(dir_path + "/")
        fout = fout + '.txt'

    def ocr(self):
        global dtout
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        dtout = pytesseract.image_to_string(Image.open(fname), 'rus+eng+chi_tra+jpn')
        self.ui.textOut.setText(dtout)

    def save_f(self):
        if dtout == '':
            self.ui.mylabel.setText(f"Файл не распознан")
        elif dtout != '':
            out  = self.ui.textOut.toPlainText()
            with open(fout, 'w') as f_out:
                f_out.write(out + "\n")
                self.ui.mylabel.setText('Файл сохранен: ' + fout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    pal = window.palette()
    #window.setFixedSize(656, 320)
    window.setWindowTitle("Gui for tesseract")
    window.setWindowIcon(QtGui.QIcon(f"{cwd}/fontmanager.png")) 
    window.show()
    sys.exit(app.exec_())
    
