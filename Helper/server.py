import random
import string
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()


def server_authentication(bearer_token:str):
    salt = os.environ["SERVER_SALT"].encode("utf-8")
    hashed_pw = os.environ["SERVER_HASHED"].encode("utf-8")

    if bcrypt.hashpw(bearer_token.encode("utf-8"), salt) == hashed_pw:
        return True
    else:
        return False