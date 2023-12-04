from PySide6.QtCore import QObject, Signal
from dbmanager import DBManager
from filemanager import FileManager
from hash import Hash
from dataconnection import DataConnection

class CommandExecuter(QObject):
    response = Signal(str)
    logged_in_changed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_connection = parent
        self.manager = DBManager(self)
        self.file_manager = FileManager(self)
        # Need to briefly store username
        self.username = None

    def execute_command(self, full_command):
        command, parameter = self.parse_command(full_command)
        if not command or not parameter:
            print("Invalid command or parameter: " + command + parameter)
            self.response.emit('501 Syntax error in parameters or arguments')
            return
        
        if command == 'USER':
            self.user(parameter)
        elif command == 'PASS':
            self.password(parameter)
        # Make directory relative to current directory
        elif command == 'MKD':
            self.mkdir(parameter)
        # Store file data on server
        elif command == 'STOR':
            self.stor(parameter)
        # List files in current directory
        elif command == 'NLST':
            self.list(parameter)
        # Retrieve a copy of the file
        elif command == 'RETR':
            self.copy(parameter)

        elif command == 'QUIT':
            self.quit()

    def parse_command(self, full_command):
        str_command = str(full_command)
        split_command = str_command.split(' ')
        if len(split_command) <= 0:
            return None, None
        
        command = split_command[0]
        parameter = split_command[1]
        return command, parameter

    def user(self, parameter):
        user_query = "SELECT username FROM users WHERE username='" + parameter + "'"
        ret = self.manager.execute_query(user_query)
        if not ret:
           msg = '430 Invalid username or password'
           print(msg)
           self.response.emit(msg)
           return

        print(ret)
        msg = '331 User name okay, need password'
        self.username = parameter
        self.response.emit(msg)

    def password(self, parameter):
        # Need to get salt, hash, then compare with stored password
        salt_query = "SELECT salt FROM users WHERE username='" + self.username + "'"
        response = self.manager.execute_query(salt_query)
        salt = response[0][0]
        password = Hash.hash_with_salt(parameter, salt)
        pass_query = "SELECT pw FROM users WHERE pw='" + password + "'"
        response = self.manager.execute_query(pass_query)
        if not response:
            msg = '430 Invalid username or password'
            print(msg)
            self.response.emit(msg)
            return
        
        msg = '230 User logged in, proceed'
        print(msg)
        self.logged_in = True
        self.handle_logged_in()
        self.response.emit(msg)

    def handle_logged_in(self):
        if not self.logged_in:
            return

        root_query = "SELECT rootDirectory FROM users WHERE username='" + self.username + "'"
        ret = self.manager.execute_query(root_query)
        root_dir = ret[0][0]
        self.file_manager.set_root_dir(root_dir)

    def mkdir(self, parameter):
        self.file_manager.create_dir(parameter)
    
    def stor(self, parameter):
        self.data_connection = DataConnection(1235, self.file_manager, parameter, self)
        self.data_connection.response.connect(self.response.emit)
        self.data_connection.transfer_finished.connect(self.close_data_connection)
        self.response.emit()

    def list(self, parameter):
        pass

    def copy(self, parameter):
        pass

    def quit(self):
        # Destroy connection and clean up
        pass

    def close_data_connection(self):
        self.data_connection = None
