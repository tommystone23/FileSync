from PySide6.QtCore import QObject, Slot, QByteArray, Signal
from PySide6.QtNetwork import QSslSocket
from responseparser import ResponseParser

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
        self.response_parser = ResponseParser(self)

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
        return not self.pending_commands