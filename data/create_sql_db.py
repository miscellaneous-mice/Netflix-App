import os
import urllib
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD_UPDATED+'@'+DATABASE_HOST+'/'+DATABASE_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

class Shows(base):
    __tablename__ = "data"
    show_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    title = Column(String)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(String)
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)
    description = Column(String)

class ShowsVerify(BaseModel):
    # show_id: int
    type: str
    title: str
    director: str
    cast: str
    country: str
    date_added: str
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: str
