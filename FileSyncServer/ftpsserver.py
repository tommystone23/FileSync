from PySide6.QtCore import QObject
from controlconnection import ControlConnection

class FTPSServer(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.control_connection = ControlConnection(1234)