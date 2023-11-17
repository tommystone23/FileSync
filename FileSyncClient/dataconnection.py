from PySide6.QtCore import QObject, QTimer, Slot, QByteArray
from PySide6.QtNetwork import QSslSocket, QSslConfiguration

class DataConnection(QObject):
    def __init__(self, host, data, parent=None):
        super().__init__(parent)
        self.data_socket = QSslSocket()
        self.port = 22
        self.data_socket.ignoreSslErrors()
        config = self.data_socket.sslConfiguration()
        config.addCaCertificates("certs/client_ca.pem")
        self.data_socket.setPrivateKey("certs/server_local.key")
        self.data_socket.setLocalCertificate("certs/server_local.pem")
        self.data_socket.setPeerVerifyMode(QSslSocket.VerifyPeer)
        self.data_socket.sslErrors.connect(self.ssl_errors)
        self.data_socket.connectToHostEncrypted(host, self.port)
        if not self.data_socket.waitForEncrypted():
            print("Failed to make Control connection")
            return False

    @Slot()
    def ssl_errors(self, errors):
        print(errors)
        self.data_socket.ignoreSslErrors()