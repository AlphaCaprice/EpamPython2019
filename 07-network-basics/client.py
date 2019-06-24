import sys
import socket
import time
import threading

import window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit,QAction, QFileDialog, QApplication, QToolBar


class Client:
    def __init__(self, server: tuple):
        self.server = server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.nickname = ""
        self.online = False

    def start(self):
        self.client_socket.connect(self.server)
        self.client_socket.sendto(self.nickname.encode("utf-8"), self.server)
        self.online = True

    def send_msg(self, msg):
        try:
            if msg:
                self.client_socket.sendto(msg.encode(), self.server)
                if msg == r"\exit":
                    self.online = False
        except ConnectionError:
            self.client_socket.sendto(r"\exit".encode("utf-8"), self.server)
            self.online = False


class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        self.client = Client(("192.168.0.100", 4242))

    def initUI(self):
        self.ui.pushButton.clicked.connect(self.send_msg)

    def send_msg(self):
        msg = self.ui.lineEdit.text()
        if not self.client.online:
            self.client.nickname = msg
            self.client.start()
            receive_thread = threading.Thread(target=self.receive_msg)
            receive_thread.start()
            self.ui.textEdit.append("You are join to chat!")
        else:
            self.ui.textEdit.append(f"You > {msg}")
            self.client.send_msg(msg)
            if msg == r"\exit":
                self.exec_()
        self.ui.lineEdit.clear()

    def receive_msg(self):
        while self.client.online:
            data, addr = self.client.client_socket.recvfrom(1024)
            self.ui.textEdit.append(data.decode())
            time.sleep(0.2)

    def closeEvent(self, event):
        self.client.send_msg(r"\exit")
        self.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
