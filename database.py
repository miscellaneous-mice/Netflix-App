import os
import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD_UPDATED+'@'+DATABASE_HOST+'/'+DATABASE_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
