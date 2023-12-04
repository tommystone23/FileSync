from PySide6.QtNetwork import QSslSocket
from PySide6.QtCore import Signal, Slot, QByteArray
from sslserver import SslServer

class SecureConnection(SslServer):
    connected = Signal()
    connection_failed = Signal()
    def __init__(self, port, parent=None):
        super().__init__(port, parent)
        self.socket = None
        self.port = port
        self.incoming_connection.connect(self.init)

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
                self.connection_failed.emit()
                return False
            self.connected.emit()
            return True
        else:
            self.connection_failed.emit()
            return False
        
    @Slot(str)
    def write_data(self, data):
        if not self.is_connected():
            return False
        self.socket.write(QByteArray(data))
        return True

    @Slot()
    def read_data(self):
        client_data = self.socket.readAll().data()
        
    def is_connected(self):
        open = self.socket.isOpen()
        encrypted = self.socket.isEncrypted() 
        return (open and encrypted)

    @Slot(list)
    def ssl_errors(self, errors):
        print(errors)
        self.socket.ignoreSslErrors()