# This Python file uses the following encoding: utf-8
from PySide6 import QtQuick
from PySide6.QtCore import Slot, QThread, QObject
from sslclient import SslClient


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = SslClient("127.0.0.1")
        self.thread = QThread()
        self.client.moveToThread(self.thread)
        self.thread.started.connect(self.client.init)
        self.thread.start()

    @Slot(str)
    def send_data(self, string):
        self.client.write_data(string)
