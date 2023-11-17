from PySide6.QtCore import QObject, Signal
from dbmanager import DBManager
from hash import Hash

class CommandExecuter(QObject):
    response_changed = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_connection = parent
        self.manager = DBManager(self)
        # Need to briefly store username
        self.username = None

    def execute_command(self, full_command):
        command, parameter = self.parse_command(full_command)
        if not command or not parameter:
            print("Invalid command or parameter: " + command + parameter)
            return
        
        if command == "USER":
            self.user(parameter)
        elif command == "PASS":
            self.password(parameter)

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
           print("Incorrect username provided")
           msg = "430 Invalid username or password"
           self.response(msg)
           return

        print(ret)
        msg = "331 User name okay, need password"
        self.username = parameter
        self.response(msg)

    def password(self, parameter):
        # Need to get salt, hash, then compare with stored password
        salt_query = "SELECT salt FROM users WHERE username='" + self.username + "'"
        response = self.manager.execute_query(salt_query)
        salt = response[0][0]
        password = Hash.hash_with_salt(parameter, salt)
        print(password)
        pass_query = "SELECT pw FROM users WHERE pw='" + password + "'"
        response = self.manager.execute_query(pass_query)
        print(response)
        if not response:
            print("Incorrect password provided")
            msg = "430 Invalid username or password"
            self.response(msg)
            return
        
        msg = "230 User logged in, proceed"
        self.username = None
        self.response(msg)

    def response(self, message):
        self.response_changed.emit(message)
