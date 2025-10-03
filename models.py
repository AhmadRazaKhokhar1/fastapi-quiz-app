# The following imports are types for Database
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
from database import Base

# Making a table inside DB for Questions
class Questions(Base):
    __tablename__ = "questions" # declare the tablename
    # declare each column
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    
class Choices(Base):
    __tablename__ = "choices"
    
    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, unique=True, index=True, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)