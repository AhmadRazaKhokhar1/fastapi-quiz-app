from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, db_dependency
from auth import router as auth_router, get_current_user
from starlette import status
from helpers.logger import logger
from middlewares.tracker_middleware import register_tracker_middleware
# This will create an app just like we do with expressJs const app = express()
app = FastAPI()
app.include_router(router=auth_router)
register_tracker_middleware(app)
# This will create all the tables and columns inside Postgres
models.Base.metadata.create_all(bind=engine)

# These are the base classes or Pydantic Models
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
    
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

user_dependency = Annotated[dict, Depends(get_current_user)]
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

@app.get("/questions/{question_id}")
async def get_question_by_id(question_id:int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No question found.")
    return result

@app.get("/choices/{question_id}")
async def get_choices_by_question_id(question_id:int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        logger.debug(f"No choices found {result}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No choices found.")
    return result

@app.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed.")
    else:
        logger.info(user)
        return { "user" : user }