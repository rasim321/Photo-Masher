from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#couldn't use the config.py file because streamlit and uvicorn are throwing
#different errors for the kind of file import
#Uvicorn doesn't like "from database" and streamlit doesn't like "from .database"
from pydantic import BaseSettings

class Settings(BaseSettings):
    # database_username: str
    # database_password: str 
    # database_hostname: str
    # database_name: str
    # database_port: str
    database_url: str
    
    class Config:
        env_file = ".env"
     
settings = Settings() 

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

SQLALCHEMY_DATABASE_URL = settings.database_url

# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@hostname:port/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def return_max_content_id():
    with engine.connect() as con:

        rs = con.execute('SELECT id FROM images WHERE id = (SELECT MAX(id) FROM images)')

        for row in rs:
            return row[0]

        con.close()

def return_max_style_id():
    with engine.connect() as con:

        rs = con.execute('SELECT id FROM styles WHERE id = (SELECT MAX(id) FROM styles)')

        for row in rs:
            return row[0]

        con.close()

