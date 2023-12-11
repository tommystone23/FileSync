# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Signal, QFile, QIODevice
from PySide6.QtNetwork import QTcpServer, QHostAddress
from PySide6.QtNetwork import QSslCertificate, QSslKey, QSsl

class SslServer(QTcpServer):
    incoming_connection = Signal(int, QSslKey, QSslCertificate)
    def __init__(self, port, parent=None):
        super().__init__(parent)
        if not QFile.exists("/home/tommy/projects/file_sync/certs/client_local.key"):
            print('File does not exist')
        key_file = QFile("/home/tommy/projects/file_sync/certs/client_local.key")
        if not key_file.open(QIODevice.OpenModeFlag.ReadOnly):
            print('Failed to open file key_file')
        self.key = QSslKey(key_file.readAll(), QSsl.Rsa)
        #key_file.close()

        if not QFile.exists("/home/tommy/projects/file_sync/certs/client_local.pem"):
            print('File does not exist')
        cert_file = QFile("/home/tommy/projects/file_sync/certs/client_local.pem")
        if not cert_file.open(QIODevice.OpenModeFlag.ReadOnly):
            print('Failed to open file cert_file')
        self.cert = QSslCertificate(cert_file.readAll())
        #cert_file.close()
        print("Listening for Connection")
        if not self.listen(QHostAddress.Any, port):
            print(self.errorString())

    def incomingConnection(self, handle):
        self.incoming_connection.emit(handle, self.key, self.cert)
