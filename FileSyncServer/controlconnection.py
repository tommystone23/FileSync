from PySide6.QtCore import QObject, Slot, QByteArray
from commandexecuter import CommandExecuter
from secureconnection import SecureConnection

class ControlConnection(SecureConnection):
    def __init__(self, port, parent=None):
        super().__init__(port, parent)
        self.connected.connect(self.on_connected)
        self.connection_failed.connect(self.on_failed_connection)
        
    def on_connected(self):
        self.cmd_exec = CommandExecuter(self)
        self.cmd_exec.response_changed.connect(self.write_data)
        self.data_connection = None
        self.get_credentials()

    def on_failed_connection(self):
        msg = '421 Service not available, closing control connection'
        self.write_data(msg)
        self.deleteLater()
        
    # Start login process
    def get_credentials(self):
        message = '332 Need account for login.'
        self.write_data(message)

    @Slot()
    def read_data(self):
        client_data = self.socket.readAll().data()
        decoded_str = str(client_data.decode("utf-8"))
        self.cmd_exec.execute_command(decoded_str)

    