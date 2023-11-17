from PySide6.QtCore import QObject, Signal

class ResponseParser(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_connection = parent

    def parse_response(self, response):
        split_response = response.split(' ')
        if len(split_response) <= 0:
            return
        
        code = int(split_response[0])
        message = ' '.join(split_response[1:len(split_response)])
        if code <= 0:
            return
        
        pending_commands = False
        logged_in = False
        error_string = None
        
        print(message)

        # The requested action is being initiated, expect another 
        # reply before proceeding with a new command.
        if code >= 100 and code < 200:
            pending_commands = True
        # The requested action has been successfully completed.
        elif code >= 200 and code < 300:
            # User logged in, proceed
            if code == 230:
                logged_in = True
            pending_commands = False
        # The command has been accepted, but the requested action is on hold, 
        # pending receipt of further information.
        elif code >= 300 and code < 400:
            conn = self.control_connection
            # User name okay, need password. 
            if code == 331:
                password = conn.password
                conn.write_data("PASS " + password)
            # Need account for login. 
            elif code == 332:
                username = conn.username
                conn.write_data("USER " + username)
        # The command was not accepted and the requested action did not take place, 
        # but the error condition is temporary and the action may be requested again.
        elif code >= 400 and code < 500:
            # Invalid username or password
            if code == 430:
                logged_in = False
                print(message)
                # Should add some thread destruction 
                # and stop connection attempts
                self.control_connection.disconnected.emit()

            pending_commands = False
            error_string = message
        # Syntax error, command unrecognized and the requested action did not take place. 
        # This may include errors such as command line too long.
        elif code >= 500 and code < 600:
            pending_commands = False
        # Replies regarding confidentiality and integrity
        elif code >= 600 and code < 700:
            pending_commands = False

        return pending_commands, logged_in, error_string