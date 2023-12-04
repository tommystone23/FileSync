from PySide6.QtCore import QObject, QDir, QJsonArray, QJsonDocument, QFile, QIODevice

class FileManager(QObject):
    # Use current home directory for testing, will need to change
    base_dir = '/home/tommy/projects/file_sync/user_files/'
    def __init__(self, parent: QObject=None):
        super().__init__(parent)
        self.root = None
        self.dir_handler = QDir()

    def set_root_dir(self, dir):
        dir = self.base_dir + dir
        self.root = dir
        self.dir_handler.setCurrent(dir)
    
    def change_dir(self, dir):
        cur_dir_name = self.dir_handler.current().dirName()
        if cur_dir_name == self.root and dir == '..':
            return False
        if not self.dir_handler.cd(dir):
            return False
        return True
    
    def create_dir(self, dir):
        self.dir_handler.mkdir(dir)

    def create_file(self, file):
        dir_path = self.dir_handler.currentPath()
        file_path = dir_path + file
        file = QFile(file_path)
        file.open(QIODevice.OpenModeFlag.WriteOnly)
        return file

    def get_dir_list_json(self):
        cur_dir = self.dir_handler.entryInfoList()
        entry_list = []
        for entry in cur_dir:
            entry_map = {}
            is_dir = entry.isDir()
            name = entry.fileName()
            entry_map['name'] = name
            entry_map['is_dir'] = is_dir

            entry_list.append(entry_map)

        json_array = QJsonArray.fromVariantList(entry_list)
        json_doc = QJsonDocument()
        json_doc.setArray(json_array)
        json = json_doc.toJson(QJsonDocument.JsonFormat.Compact)

        return json
        