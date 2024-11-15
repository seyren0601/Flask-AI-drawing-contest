from DB import db
from Helper import user
def get_all_user():
    users = db.GET_all_users()
    return users

def create_user():
    username = f"usr{len(db.GET_all_users()):05}"    
    password = user.random_password()
    group_id = 3
    salt , hashed_pw = user.hash_password(password)    
    new_user = db.CREATE_user(username,group_id,salt,hashed_pw)
    return new_user

