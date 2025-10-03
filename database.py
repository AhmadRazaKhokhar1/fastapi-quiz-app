from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os 
from typing import Annotated
from fastapi import Depends

load_dotenv(dotenv_path=".env.local")

DB_URL = os.getenv('POSTGRESQL_DB_URL')
print(f"DB URL ====> {DB_URL}")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    # produces new DB session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]