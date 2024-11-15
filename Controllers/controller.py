from DB import db

def get_all_user():
    users = db.GET_all_users()
    return users

def get_all_teams():
    teams = db.GET_all_teams()
    return teams