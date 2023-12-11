# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QTimer, Slot, QObject, QMutex, QByteArray, QThread, Signal
from controlconnection import ControlConnection

class FTPSClient(QObject):
    disconnected = Signal()
    file_list_changed = Signal(str)
    def __init__(self, host, username, password, parent=None):
        super().__init__(parent)
        self.host = host
        self.username = username
        self.password = password

    def init(self):
        self.control_connection = ControlConnection(self.host, self.username, self.password, self)
        self.control_connection.disconnected.connect(self.disconnected.emit)
        self.control_connection.response_parser.file_list_changed.connect(self.file_list_changed.emit)
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
            data = self.data_queue[0]
            if not self.control_connection.has_pending_commands():
                if data.startswith('STOR'):
                    split_command = data.split(' ')
                    self.set_filename(split_command[1].split('-')[0])
                self.control_connection.write_data(QByteArray(data))
                self.data_queue.pop(0)
        self.mutex.unlock()

        QThread.sleep(1)
        QTimer.singleShot(0, self.do_run_iteration)
        
    def write_data(self, data : str):
        self.mutex.lock()
        self.data_queue.append(data)
        self.mutex.unlock()
    
    def set_filename(self, filename):
        self.control_connection.cur_filename = filename
