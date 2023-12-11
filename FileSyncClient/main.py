# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from controller import Controller
from filelistmodel import FileListModel

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    # qmlRegisterType(controller.Controller, "Controller", 1, 0, "Controller")
    # qmlRegisterType(filelistmodel.FileListModel, "FileListModel", 1, 0, "FileListModel")
    server_file_model = FileListModel()
    controller = Controller(server_file_model)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)
    engine.rootContext().setContextProperty("server_file_model", server_file_model)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
