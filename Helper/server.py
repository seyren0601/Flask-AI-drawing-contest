import random
import string
import bcrypt

def server_authentication(bearer_token:str):
    salt = b"$2b$12$QWtjgUEzesM0B4Kr2qqSeO"
    hashed_pw = b"$2b$12$QWtjgUEzesM0B4Kr2qqSeOyd16C0CQIZAiNuyS1nzxLuA0lWpZney"

    if bcrypt.hashpw(bearer_token.encode("utf-8"), salt) == hashed_pw:
        return True
    else:
        return False