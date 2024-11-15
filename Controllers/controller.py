from DB import db

def get_all_user():
    users = db.GET_all_users()
    return users

def get_user(user_id):
    user = db.GET_user(user_id)
    return user

def get_all_teams():
    teams = db.GET_all_teams()
    return teams

def get_team(team_id):
    team = db.GET_team(team_id)
    return team