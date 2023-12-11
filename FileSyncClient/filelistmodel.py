# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, Property, Signal, Slot

class FileListModel(QAbstractListModel):
    dataChanged = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []
        self.is_dir = Qt.UserRole + 1
        self.name = Qt.UserRole + 2
        self.RoleNames = {
            self.is_dir: b"is_dir",  # Custom role names
            self.name: b"name"
        }

    def data(self, index : QModelIndex, role):
        if (0 <= index.row() < self.rowCount()):
            if role == self.is_dir:
                item = self.items[index.row()]['is_dir']
            elif role == self.name:
                item = self.items[index.row()]['name']
            return item

    def roleNames(self) -> dict[int, QByteArray]:
        return self.RoleNames

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self.items)
    
    @Slot(list)
    def change_list(self, list_items):
        self.beginResetModel()
        self.items = list_items
        self.endResetModel()
        self.dataChanged.emit()