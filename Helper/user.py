import random
import string
import bcrypt

def random_password(length=5):
    password = ''.join(random.choices(string.ascii_letters),length)
    return password

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
    return salt , hashed_pw