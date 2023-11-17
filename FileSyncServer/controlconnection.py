from PySide6.QtCore import QObject, Slot, QByteArray
from PySide6.QtNetwork import QSslSocket
from commandexecuter import CommandExecuter

class ControlConnection(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = None

    def init(self, handle, key, cert):
        self.authorized = False
        self.socket = QSslSocket(self)
        self.socket.sslErrors.connect(self.ssl_errors)
        if self.socket.setSocketDescriptor(handle):
            self.socket.setPrivateKey(key)
            self.socket.setLocalCertificate(cert)
            config = self.socket.sslConfiguration()
            config.addCaCertificates("certs/server_ca.pem")
            self.socket.setPeerVerifyMode(QSslSocket.VerifyPeer)
            self.socket.readyRead.connect(self.read_data)
            self.socket.startServerEncryption()
            if not self.socket.waitForEncrypted():
                print("Failed to make encrypted connection")
                return False
            self.cmd_exec = CommandExecuter(self)
            self.cmd_exec.response_changed.connect(self.write_data)
            self.data_connection = None
            self.get_credentials()
            return True
        else:
            return False
        
    # Start login process
    def get_credentials(self):
        message = "332 Need account for login."
        self.write_data(message)

    @Slot(str)
    def write_data(self, data):
        if not self.is_connected():
            return False
        self.socket.write(QByteArray(data))
        return True

    @Slot()
    def read_data(self):
        client_data = self.socket.readAll().data()
        decoded_str = str(client_data.decode("utf-8"))
        self.cmd_exec.execute_command(decoded_str)
        
    def is_connected(self):
        open = self.socket.isOpen()
        encrypted = self.socket.isEncrypted() 
        return (open and encrypted)

    @Slot(list)
    def ssl_errors(self, errors):
        print(errors)
        self.socket.ignoreSslErrors()

    