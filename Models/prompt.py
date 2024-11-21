from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Prompt(db.Model):
    __tablename__ = "prompts"
    # Prompt info
    prompt_id: Mapped[int] = mapped_column(primary_key=True)
    prompt: Mapped[str]
    image: Mapped[str]
    date_time: Mapped[str]
    
    # Submission info
    # submitted: Mapped[bool]
    # submit_date: Mapped[str]
    # assigned: Mapped[bool]
    
    # Relationships
    team_id: Mapped[int] = mapped_column(ForeignKey('User.user_id'))
    
    def toJson(self):
        return {
            "prompt_id":self.prompt_id,
            "prompt":self.prompt,
            "image":self.image,
            "date_time":str(self.date_time),
            "team_id":self.team_id
            # "submitted":self.submitted,
            # "submit_date":self.submit_date,
            # "assigned":self.assigned
        }