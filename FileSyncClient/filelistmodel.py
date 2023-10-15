# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QAbstractListModel


class FileListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sort_reversed = False
        self.show_files = True
        self.show_dirs = False
        self.show_dirs_first = False
        self.show_dot_and_dot_dot = False
        self.show_only_readable = False
        self.show_hidden = False

    def data(index, role):
        pass
