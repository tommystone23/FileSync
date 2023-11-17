import hashlib
import random
import string

class Hash():
    @staticmethod
    def hash_and_salt(message):
        salt = Hash.create_salt()
        pw_and_salt = message + salt
        hash = hashlib.sha256(pw_and_salt.encode('UTF-8')).hexdigest()
        return hash.strip(), salt.strip()
    
    @staticmethod
    def hash_with_salt(message, salt):
        pw_and_salt = message + salt
        hash = hashlib.sha256(pw_and_salt.encode('UTF-8')).hexdigest()
        return hash

    @staticmethod
    def create_salt(length=64):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

