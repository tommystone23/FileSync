# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Signal, QFile, QIODevice
from PySide6.QtNetwork import QTcpServer, QHostAddress
from PySide6.QtNetwork import QSslCertificate, QSslKey, QSsl
from controlconnection import ControlConnection

class SslServer(QTcpServer):
    incoming_connection = Signal(int, QSslKey, QSslCertificate)
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
        self.incoming_connection.emit(handle, self.key, self.cert)
