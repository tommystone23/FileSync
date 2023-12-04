# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from ftpsserver import FTPSServer

if __name__ == "__main__":
    app = QApplication([])

    server = FTPSServer()

    sys.exit(app.exec())
