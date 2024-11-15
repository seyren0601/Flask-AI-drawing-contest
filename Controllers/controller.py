from DB import db

def get_all_user():
    users = db.GET_all_users()
    return users