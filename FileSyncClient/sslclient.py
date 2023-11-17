# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QTimer, Slot, QObject, QMutex, QByteArray, QThread, Signal
from controlconnection import ControlConnection


class SslClient(QObject):
    disconnected = Signal()
    def __init__(self, host, username, password, parent=None):
        super().__init__(parent)
        self.host = host
        self.username = username
        self.password = password

    def init(self):
        self.control_connection = ControlConnection(self.host, self.username, self.password, self)
        self.control_connection.disconnected.connect(self.disconnected.emit)
        self.data_queue = []
        self.mutex = QMutex()
        QTimer.singleShot(0, self.do_run_iteration)

    @Slot()
    def do_run_iteration(self):
        if not self.control_connection.is_connected():
            QThread.sleep(1)
            if not self.control_connection.connect_host():
                print("Failed to connect to host")
            QTimer.singleShot(0, self.do_run_iteration)
            return
        
        self.mutex.lock()
        if len(self.data_queue):
            print("Write to Socket")
            data = self.data_queue[0]
            if not self.control_connection.has_pending_commands():
                self.control_connection.write_data(QByteArray(data))
            self.data_queue.pop(0)
        self.mutex.unlock()

        QThread.sleep(1)
        QTimer.singleShot(0, self.do_run_iteration)
        
    def write_data(self, data):
        self.mutex.lock()
        self.data_queue.append(data)
        self.mutex.unlock()
