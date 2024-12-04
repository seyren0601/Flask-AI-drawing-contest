from DAL import db

def authenticate_session(session_token):
    user = db.GET_user_from_token(session_token)
    return user