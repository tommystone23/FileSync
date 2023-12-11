from PySide6.QtCore import QObject, Slot, QByteArray, Signal, QTimer, QFile, QIODevice, QElapsedTimer
from PySide6.QtNetwork import QSslSocket
from responseparser import ResponseParser
from dataconnection import DataConnection

class ControlConnection(QObject):
    disconnected = Signal()
    def __init__(self, host, username, password, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = 1234
        self.username = username
        self.password = password
        self.pending_commands = False
        self.error_string = None
        self.logged_in = False
        self.connection_socket = QSslSocket(self)
        self.connection_socket.disconnected.connect(self.disconnected.emit)
        self.response_parser = ResponseParser(self)
        self.cur_filename = None # Name of file being sent
        self.bytes_written = 0
        self.response_parser.data_connection_request.connect(self.handle_data_connection)

    def connect_host(self):
        self.connection_socket.ignoreSslErrors()
        config = self.connection_socket.sslConfiguration()
        config.addCaCertificates("certs/client_ca.pem")
        self.connection_socket.setPrivateKey("certs/server_local.key")
        self.connection_socket.setLocalCertificate("certs/server_local.pem")
        self.connection_socket.sslErrors.connect(self.ssl_errors)
        self.connection_socket.readyRead.connect(self.read_data)
        self.connection_socket.connectToHostEncrypted(self.host, self.port)
        if not self.connection_socket.waitForEncrypted():
            print(self.connection_socket.errorString())
            return False
        
        self.pending_commands = False
        return True
    
    def write_data(self, data):
        if not self.is_connected():
            return False
        self.connection_socket.write(QByteArray(data))
        self.pending_commands = True

        return True

    @Slot()
    def read_data(self):
        server_data = self.connection_socket.readAll().data()
        self.process_response(server_data.decode("utf-8"))

    def process_response(self, response):
        a, b, c = self.response_parser.parse_response(response)
        self.pending_commands = a
        self.logged_in = b
        self.error_string = c

    @Slot()
    def ssl_errors(self, errors):
        print(errors)
        self.connection_socket.ignoreSslErrors()

    def is_connected(self):
        open = self.connection_socket.isOpen()
        encrypted = self.connection_socket.isEncrypted()
        
        return (open and encrypted)
    
    # Ready for new commands
    def has_pending_commands(self):
        return self.pending_commands
    
    @Slot()
    def handle_data_connection(self):
        self.data_connection = DataConnection('127.0.0.1')
        if not self.data_connection.init():
            self.data_connection.deleteLater()
            self.data_connection = None
            error_string = 'Could not initiate data connection'
            return self.pending_commands, self.logged_in, error_string
        print('Data connection opened')
        self.file = QFile(self.cur_filename)
        print("File name: " + self.cur_filename)
        if not self.file.open(QIODevice.OpenModeFlag.ReadOnly):
            print("Failed to open file for reading")
            return
        self.cur_filename = None
        self.timer = QElapsedTimer()
        self.timer.start()
        self.do_write_data()

    # Write data to data connection
    @Slot()
    def do_write_data(self):
        data_size = 1500
        data = self.file.read(data_size)
        self.bytes_written += data.size()
        if data:
            self.data_connection.write_data(data)
            if self.timer.elapsed() >= 1000:
                percentage = (self.bytes_written / self.file.size()) * 100
                print(self.cur_filename + '... ' + str(percentage) + '%')
            QTimer.singleShot(0, self.do_write_data)
        else:
            print('Closing Data Connection')
            self.data_connection.deleteLater()
            self.data_connection = None
            self.timer = None
            self.bytes_written = 0
            self.file.close()
