# This Python file uses the following encoding: utf-8
from PySide6 import QtQuick
from PySide6.QtCore import Slot, QThread, QObject
from sslclient import SslClient


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)


    @Slot(str, str, str)
    def connect_host(self, host, username, password):
        self.client = SslClient(host, username, password)
        self.client_thread = QThread()
        self.client.moveToThread(self.client_thread)
        self.client_thread.started.connect(self.client.init)
        self.client_thread.start()

    @Slot(str)
    def send_data(self, string):
        self.client.write_data(string)
