# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QTimer, Slot, QObject, QMutex, QByteArray
from PySide6.QtNetwork import QSslSocket, QSslConfiguration


class SslClient(QObject):
    def __init__(self, host, parent=None):
        super().__init__(parent)
        self.host = host
        self.data_queue = []
        self.mutex = QMutex()

    def init(self):
        self.socket_connect()
        QTimer.singleShot(0, self.do_run_iteration)

    @Slot()
    def do_run_iteration(self):
        if not self.socket.isOpen():
            self.socket_connect()
        self.mutex.lock()
        if len(self.data_queue):
            print("Write to Socket")
            data = self.data_queue.pop(0)
            self.socket.write(QByteArray(data))
        self.mutex.unlock()

        QTimer.singleShot(0, self.do_run_iteration)

    def socket_connect(self):
        self.socket = QSslSocket(self)
        self.socket.ignoreSslErrors()
        config = self.socket.sslConfiguration()
        config.addCaCertificates("../certs/client_ca.pem")
        self.socket.setPrivateKey("../certs/server_local.key")
        self.socket.setLocalCertificate("../../certificates/server_local.pem")
        self.socket.setPeerVerifyMode(QSslSocket.VerifyPeer)
        self.socket.sslErrors.connect(self.ssl_errors)
        self.socket.readyRead.connect(self.read_data)
        self.socket.connectToHostEncrypted(self.host, 1234)
        if not self.socket.waitForEncrypted():
            print(self.socket.errorString())

    def write_data(self, data):
        self.mutex.lock()
        self.data_queue.append(data)
        self.mutex.unlock()

    @Slot()
    def read_data(self):
        server_data = self.socket.readAll().data()
        print(server_data)

    @Slot()
    def ssl_errors(self, errors):
        print(errors)
        self.socket.ignoreSslErrors()
