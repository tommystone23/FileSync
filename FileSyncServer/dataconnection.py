from PySide6.QtCore import Signal, Slot, QIODevice
from secureconnection import SecureConnection
from filemanager import FileManager

class DataConnection(SecureConnection):
    transfer_finished = Signal()
    response = Signal(str)
    def __init__(self, port, file_manager : FileManager, parameter : str, parent=None):
        super().__init__(port, parent)
        self.file_manager = file_manager
        # Send in format FILENAME_FILESIZE
        file_name = parameter.split('-')[0]
        self.file_size = int(parameter.split('-')[1])
        self.file = file_manager.create_file(file_name)
        self.bytes_written = 0
        self.connected.connect(self.on_connected)
        self.connection_failed.connect(self.on_failed_connection)
        self.response.emit('150 File status okay; about to open data connection.')

    def on_connected(self):
        pass

    def on_failed_connection(self):
        pass

    @Slot()
    def read_data(self):
        while True:
            file_data = self.socket.readAll()
            self.bytes_written += file_data.size()
            print('Writing ' + str(file_data.size()) + 'bytes')
            if not self.file.write(file_data):
                self.response.emit('451 Requested action aborted. Could not write data to file.')
                break
            if self.bytes_written == self.file_size:
                break
        self.transfer_finished.emit()
        self.file.close()
        self.deleteLater()
