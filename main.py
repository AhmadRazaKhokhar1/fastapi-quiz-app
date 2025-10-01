from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# This will create an app just like we do with expressJs const app = express()
app = FastAPI()

# This will create all the tables and columns inside Postgres
models.Base.metadata.create_all(bind=engine)

# These are the base classes or Pydantic Models
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
    
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
def get_db():
    # produces new DB session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# API routes and controllers
@app.post('/questions')
async def create_questions(question: QuestionBase, db: db_dependency):
     db_question = models.Questions(question_text=question.question_text)
     db.add(db_question)
     db.commit()
     db.refresh(db_question)
     
     for choice in question.choices:
         db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
         db.add(db_choice)
         db.commit()
         db.refresh(db_choice)