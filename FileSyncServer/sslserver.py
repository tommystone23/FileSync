# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, SIGNAL, SLOT, QFile, QIODevice
from PySide6.QtNetwork import QTcpServer, QHostAddress
from PySide6.QtNetwork import QSslCertificate, QSslKey, QSsl
from controlconnection import ControlConnection

class SslServer(QTcpServer):
    def __init__(self, port, parent=None):
        super().__init__(parent)
        key_file = QFile("certs/client_local.key")
        key_file.open(QIODevice.ReadOnly)
        self.key = QSslKey(key_file.readAll(), QSsl.Rsa)
        key_file.close()

        cert_file = QFile("certs/client_local.pem")
        cert_file.open(QIODevice.ReadOnly)
        self.cert = QSslCertificate(cert_file.readAll())
        cert_file.close()
        print("Listening for Connection")
        if not self.listen(QHostAddress.Any, port):
            print(self.errorString())

    def incomingConnection(self, handle):
        # Just handle one incoming connection for now
        self.control_connection = ControlConnection(self)
        if self.control_connection.init(handle, self.key, self.cert):
            print("Established connection")
        else:
            print("Unable to establish connection")
