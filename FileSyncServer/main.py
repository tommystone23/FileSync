# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from sslserver import SslServer


if __name__ == "__main__":
    app = QApplication([])

    server = SslServer()

    sys.exit(app.exec())
