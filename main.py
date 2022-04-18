import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap


from rsa import initialize, process, to_hex, export, to_ascii, to_string, clean, get_size

import os
import time


class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("home.ui", self)
        self.pushButton.clicked.connect(self.Text_Encrypt)
        self.pushButton_2.clicked.connect(self.File_Encrypt)

    def init(self):
        p = int(self.lineEdit.text())
        q = int(self.lineEdit_2.text())
        global data
        data = initialize(p, q)
        # return data

    def Text_Encrypt(self):
        Menu.init(self)
        text_encrypt = Text_Encrypt()
        widget.addWidget(text_encrypt)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def File_Encrypt(self):
        Menu.init(self)
        file_encrypt = File_Encrypt()
        widget.addWidget(file_encrypt)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Text_Encrypt(QMainWindow):
    def __init__(self):
        super(Text_Encrypt, self).__init__()
        loadUi("text.ui", self)
        self.pushButton.clicked.connect(self.Menu)
        self.pushButton_2.clicked.connect(self.Compute)

    def Menu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Compute(self):
        timenow = time.time()

        global data
        plaintext = self.textEdit.toPlainText()

        # Encryption
        encrypted = process(to_ascii(clean(plaintext)), data[1], data[0])
        self.textBrowser.setText(to_hex(encrypted))

        # Export
        ciphertext = self.textBrowser.toPlainText()
        export(ciphertext)

        # Decryption
        decrypted = process(encrypted, data[2], data[0])
        self.textBrowser_2.setText(to_string(decrypted))

        # Status
        size = 'Size of file is ' + get_size() + ' bytes'
        self.label_6.setText(size)

        timelater = time.time()
        duration = str(timelater-timenow) + 's'
        self.label_4.setText(duration)


class File_Encrypt(QMainWindow):
    def __init__(self):
        super(File_Encrypt, self).__init__()
        loadUi("file.ui", self)
        self.pushButton.clicked.connect(self.Menu)
        self.pushButton_2.clicked.connect(self.Browse)
        self.pushButton_3.clicked.connect(self.Compute)

    def Menu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Browse(self):
        browser = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)")
        if browser:
            self.textBrowser.setText(os.path.basename(browser[0]))

    def Compute(self):
        timenow = time.time()

        global data
        directory = os.path.basename(self.textBrowser.toPlainText())
        print(directory)

        # Encryption
        lines = open(directory, 'rb')
        plaintext = bytearray(lines.read())
        lines.close()

        encrypted = process(plaintext, data[1], data[0])
        self.textBrowser_2.setText(to_hex(encrypted))

        lines = open(directory, 'wb')
        lines.write(bytearray(encrypted))
        lines.close()

        # Export
        ciphertext = self.textBrowser_2.toPlainText()
        export(ciphertext)

        # Decryption
        lines = open(directory, 'rb')
        plaintext = bytearray(lines.read())
        lines.close()

        decrypted = process(plaintext, data[2], data[0])

        lines = open(directory, 'wb')
        lines.write(bytearray(decrypted))
        lines.close()

        self.label_8.setText("Please check your files!")

        # Status
        size = 'Size of file is ' + get_size() + ' bytes'
        self.label_6.setText(size)

        timelater = time.time()
        duration = str(timelater-timenow) + 's'
        self.label_4.setText(duration)


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
