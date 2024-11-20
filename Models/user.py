from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()

class User(db.Model):
    # User info
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    school_name: Mapped[str]
    grade: Mapped[str]
    register_date: Mapped[str]
    team_info: Mapped[str]
    
    # Authentication
    group_id: Mapped[int]
    username: Mapped[str] = mapped_column(unique=True)
    salt: Mapped[str]
    hashed_pw: Mapped[str]
    session_token: Mapped[str]
    
    # Relationships
    prompts:Mapped[List["Prompts"]] = relationship()
    
    
    def toJSON(self):
        return {
            "user_id":self.user_id, 
            "name": self.name,
            "username":self.username,
            "school_name":self.school_name,
            "grade": self.grade,
            "email":self.email,
            "phone_number":self.phone_number,
            "group_id":self.group_id,
            "salt":self.salt,
            "hashed_pw":self.hashed_pw,
            "session_token":self.session_token,
            "register_date":str(self.register_date),
            "team_info":self.team_info,
        }