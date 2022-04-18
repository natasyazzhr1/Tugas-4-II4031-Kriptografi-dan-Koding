import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap


from digitalsignature import initialize, file_read, sign, verify

import os
import time


class Menu(QMainWindow):

    def __init__(self):
        super(Menu, self).__init__()
        loadUi("home.ui", self)
        self.pushButton.clicked.connect(self.Select_Private_Key)
        self.pushButton_2.clicked.connect(self.Select_Public_Key)
        self.pushButton_3.clicked.connect(self.Select_File_Sign)
        self.pushButton_4.clicked.connect(self.Select_File_Verify)
        self.pushButton_5.clicked.connect(self.Authenticate)
        self.pushButton_6.clicked.connect(self.Generate)
        self.pushButton_7.clicked.connect(self.Sign)

    def Generate(self):
        p = int(self.textEdit.toPlainText())
        q = int(self.textEdit_2.toPlainText())
        global n
        n = initialize(p, q)

    def Select_Private_Key(self):
        browser = QFileDialog.getOpenFileName(
            self, "Open File", "", "Pri Files (*.pri)")
        if browser:
            file_name = os.path.basename(browser[0])
            self.textBrowser.setText(file_name)

    def Select_Public_Key(self):
        browser = QFileDialog.getOpenFileName(
            self, "Open File", "", "Pub Files (*.pub)")
        if browser:
            file_name = os.path.basename(browser[0])
            self.textBrowser_2.setText(file_name)

    def Select_File_Sign(self):
        browser = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt)")
        if browser:
            file_name = os.path.basename(browser[0])
            self.textBrowser_3.setText(file_name)
            self.textBrowser_6.setText(file_read(file_name))
            self.label_3.setText("Currently viewing: " + file_name)

    def Sign(self):
        global n
        pri_name = self.textBrowser.toPlainText()
        file_name = self.textBrowser_3.toPlainText()
        sign(file_name, pri_name, n)

    def Select_File_Verify(self):
        browser = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt)")
        if browser:
            file_name = os.path.basename(browser[0])
            self.textBrowser_4.setText(file_name)
            self.textBrowser_6.setText(file_read(file_name))
            self.label_3.setText("Currently viewing: " + file_name)

    def Authenticate(self):
        global n
        pub_name = self.textBrowser_2.toPlainText()
        file_name = self.textBrowser_4.toPlainText()
        status = verify(file_name, pub_name, n)
        self.textBrowser_5.setText(status)


# main
app = QApplication(sys.argv)
welcome = Menu()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
