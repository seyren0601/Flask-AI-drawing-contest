from DB import db
from Helper import user
def get_all_user():
    users = db.GET_all_users()
    return users

def create_user():
    username = 'usr'.join(db.Count_user())
    print(username)
    password = user.random_password()
    salt , hashed_pw = user.hash_password(password)
    
    new_user = db.CREATE_user(username,salt,hashed_pw)
    return new_user

