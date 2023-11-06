from PySide6.QtCore import QObject, QTimer, Slot, QByteArray
from PySide6.QtNetwork import QSslSocket, QSslConfiguration

class ControlConnection(QObject):
    def __init__(self, host, username, password, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = 1234
        self.username = username
        self.password = password
        self.connection_socket = QSslSocket(self)

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
        self.process_response(server_data)
        print(server_data)

    def process_response(self, response):
        str_response = str(response)
        split_response = str_response.split(' ')
        if len(split_response) <= 0:
            return
        
        code = int(split_response[0])
        if code <= 0:
            return
        
        # The requested action is being initiated, expect another 
        # reply before proceeding with a new command.
        if code >= 100 and code < 200:
            self.pending_commands = True
        # The requested action has been successfully completed.
        elif code >= 200 and code < 300:
            self.pending_commands = False
        # The command has been accepted, but the requested action is on hold, 
        # pending receipt of further information.
        elif code >= 300 and code < 400:
            # User name okay, need password. 
            if code == 331:
                message = "PASS " + self.password
                self.write_data(message)
            # Need account for login. 
            elif code == 332:
                message = "USER " + self.username
                self.write_data(message)

        # The command was not accepted and the requested action did not take place, 
        # but the error condition is temporary and the action may be requested again.
        elif code >= 400 and code < 500:
            self.pending_commands = False
            self.error_code = split_response[1]
        # Syntax error, command unrecognized and the requested action did not take place. 
        # This may include errors such as command line too long.
        elif code >= 500 and code < 600:
            self.pending_commands = False
        # Replies regarding confidentiality and integrity
        elif code >= 600 and code < 700:
            self.pending_commands = False

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