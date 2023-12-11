# This Python file uses the following encoding: utf-8
from PySide6 import QtQuick
from PySide6.QtCore import Slot, QThread, QObject, QFile, QIODevice, Property, Signal, QJsonDocument, QByteArray, QDir
from ftpsclient import FTPSClient
from filelistmodel import FileListModel

class Controller(QObject):
    file_list_changed = Signal(list)
    def __init__(self, server_list_model : FileListModel, parent=None):
        super().__init__(parent)
        self.server_files = server_list_model

    @Slot(str, str, str)
    def connect_host(self, host, username, password):
        self.client = FTPSClient(host, username, password)
        self.client.disconnected.connect(self.reset)
        self.client.file_list_changed.connect(self.handle_file_list_json)
        self.client_thread = QThread()
        self.client.moveToThread(self.client_thread)
        self.client_thread.started.connect(self.client.init)
        self.client_thread.start()

    @Slot(str)
    def init_stor_cmd(self, file_path : str):
        path = file_path[7:] # Remove file:// prefix
        QDir.setCurrent(path)
        dir = QDir(path)
        if not dir.exists(path):
            print('Invalid directory ' + path)
        file_list = dir.entryInfoList()
        for entry in file_list:
            if entry.isFile() and (not entry.isDir()):
                file = QFile(entry.filePath())
                if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                    print('Failed to open file: ' + path)
                    continue
                split_file_path = entry.filePath().split('/')
                filename = split_file_path[len(split_file_path)-1]
                file_size = file.size()
                print(filename)
                print(file_size)
                msg = f'STOR {filename}-{file_size}'
                self.client.write_data(msg)
                file.close()

    @Slot()
    def get_dir_list(self):
        msg = 'NLST .'
        self.client.write_data(msg)

    @Slot(list)
    def set_list(self, file_list):
        self.server_files.change_list(file_list)

    @Slot(str)
    def handle_file_list_json(self, file_list : str):
        json_doc = QJsonDocument.fromJson(QByteArray(file_list))
        array = json_doc.array()
        self.set_list(array.toVariantList())

    @Slot()
    def reset(self):
        # Clean up client connection
        self.client_thread.exit()
        self.client_thread.wait()
        del self.client