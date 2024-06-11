import os
import urllib
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import String, Column, Integer, Date
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD_UPDATED+'@'+DATABASE_HOST+'/'+DATABASE_NAME
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD_UPDATED}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Shows(Base):
    __tablename__ = "shows"
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
