# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, SIGNAL, SLOT, QFile, QIODevice
from PySide6.QtNetwork import QTcpServer, QHostAddress, QSslSocket
from PySide6.QtNetwork import QSslCertificate, QSslKey, QSsl


class SslServer(QTcpServer):
    def __init__(self, parent=None):
        super().__init__(parent)
        key_file = QFile("../certs/client_local.key")
        key_file.open(QIODevice.ReadOnly)
        self.key = QSslKey(key_file.readAll(), QSsl.Rsa)
        key_file.close()

        cert_file = QFile("../certs/client_local.pem")
        cert_file.open(QIODevice.ReadOnly)
        self.cert = QSslCertificate(cert_file.readAll())
        cert_file.close()
        self.listen(QHostAddress.Any, 1234)

    def incomingConnection(self, handle):
        if self.init_socket(handle):
            print("Make connection")
        else:
            print("Unable to establish connection")

    def init_socket(self, handle):
        self.socket = QSslSocket()
        self.socket.sslErrors.connect(self.ssl_errors)
        if self.socket.setSocketDescriptor(handle):
            self.socket.setPrivateKey(self.key)
            self.socket.setLocalCertificate(self.cert)
            config = self.socket.sslConfiguration()
            config.addCaCertificates("../certs/server_ca.pem")
            self.socket.setPeerVerifyMode(QSslSocket.VerifyPeer)
            self.socket.readyRead.connect(self.read_data)
            self.socket.startServerEncryption()
            return True
        else:
            return False

    @Slot()
    def read_data(self):
        client_data = self.socket.readAll().data()
        print(client_data)
        self.socket.write(client_data)

    @Slot(str)
    def ssl_errors(self, errors):
        print(errors)
        self.socket.ignoreSslErrors()
