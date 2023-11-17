from PySide6.QtCore import QObject
from mysql.connector import connect, Error
from hash import Hash
import os

# Will do normal DB connections for now, can change to connection pool later
class DBManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_name = "filesyncDB"
        # Shouldn't have password as plaintext but for now is fine
        os.system("mysql --user=root --password=admin < config/db_init.sql")
        # Create default user admin/admin
        # First check if user exists
        user_check_query = "SELECT username FROM users WHERE username='admin'"
        ret = self.execute_query(user_check_query)
        if not ret:
            # Hash password with salt
            hash, salt = Hash.hash_and_salt("admin")
            print("hash length: " + str(len(hash)) + hash)
            default_user_query = f"""
            INSERT INTO users(username, pw, rootDirectory, salt)
            VALUES('admin', '{hash}', '{'admin/'}', '{salt}')
            """
            ret = self.execute_query(default_user_query)
            print(ret)

    def connect(self, db_name=None):
        try:
            connection = connect(
                host="localhost",
                user="root",
                password="admin",
                database=db_name,
            ) 
            print(connection)
            return connection
        except Error as e:
            print(e)

    def execute_query(self, query):
        if not self.db_name:
            print("No Database specified")
            return
    
        connection = self.connect(self.db_name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            ret = cursor.fetchall()
            connection.commit()
            connection.close()
            return ret

