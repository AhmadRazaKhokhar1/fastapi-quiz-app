from datetime import timedelta, datetime
from typing import Annotated, TypedDict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from main import db_dependency
load_dotenv(dotenv_path=".env.local")

JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, create_user_request:CreateUserRequest):
    print(f"create user object: ====>{create_user_request}")
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
        )
    db.add(create_user_model)
    db.commit()
    return create_user_model

@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = await authenticate_user(username=form_data.username, password=form_data.password, db=db)
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {
        "access_token":token,
        "token_type": "bearer"
    }

async def authenticate_user(username: str, password: str, db:Session):
    try:
        user = db.query(Users).filter(Users.username == username).first()
        if not user:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        is_password_correct = bcrypt_context.verify(password, user.hashed_password)
        if is_password_correct:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

def create_access_token(username, user_id, time_delta):
    encode = {
        "sub":username,
        "id":user_id
    }
    expires = datetime.utcnow() + time_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {
            "username":username,
            "id":user_id
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")