# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import controller

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    qmlRegisterType(controller.Controller, "Controller", 1, 0, "Controller")
    engine = QQmlApplicationEngine()
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
