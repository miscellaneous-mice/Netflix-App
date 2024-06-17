from pydantic import BaseModel
from schema.database import Base
from sqlalchemy import String, Column, Integer, Date
from datetime import datetime

rating_to_age = {'TV-MA': 17, 'TV-14': 14, 'PG-13': 13, 'PG': 13, 'R': 18, 'TV-PG': 13, 'G': 0, 'TV-Y7': 7,
       'TV-G': 0, 'TV-Y': 0, 'NC-17': 17, 'NR': 18, 'TV-Y7-FV': 7, 'UR': 18}

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    hashed_password = Column(String)
    country = Column(String)

class Shows(Base):
    __tablename__ = "shows"
    show_id = Column(Integer,primary_key=True)
    type = Column(String)
    title = Column(String)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)
    description = Column(String)
    age_rating = Column(Integer)

class ShowsVerify(BaseModel):
    type: str
    title: str
    director: str
    cast: str
    country: str
    date_added: datetime
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: str

