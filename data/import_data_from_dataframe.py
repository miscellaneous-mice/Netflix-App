import os
import re
from import_logger import logger
from create_sql_db import engine
from sqlalchemy import text
import pandas as pd

curr_directory = os.getcwd()


month_dict = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

age_rating = {'TV-MA': 17, 'TV-14': 14, 'PG-13': 13, 'PG': 13, 'R': 18, 'TV-PG': 13, 'G': 0, 'TV-Y7': 7,
       'TV-G': 0, 'TV-Y': 0, 'NC-17': 17, 'NR': 18, 'TV-Y7-FV': 7, 'UR': 18}

def to_date(x):
    pattern = re.compile(r'([\w]+) ([\d]+), ([\d]+)')
    date = re.search(pattern, x)
    day = date.group(2)
    month = month_dict[date.group(1)]
    year = date.group(3)
    return f'{year}-{month}-{day}'

logger.info("Importing CSV File as dataframe")
shows = pd.read_csv(curr_directory + '/data/netflix_titles.csv')
shows = shows.dropna()
logger.info("Successfully imported CSV File as dataframe")
shows['date_added'] = pd.to_datetime(shows['date_added'].apply(lambda x: to_date(x)))
breakpoint()
shows['age_rating'] = shows['rating'].apply(lambda x: age_rating[x])
shows['country'] = shows['country'].apply(lambda x: x.split(', '))
shows = shows.explode(['country'])
shows = shows.reset_index().reset_index()
shows = shows.drop(['show_id', 'index'], axis=1)
shows.rename(columns={'level_0': 'show_id'}, inplace=True)
# shows = shows.reset_index().rename(columns = {'index' : 'show_id'})
shows['release_year'] = shows['release_year'].astype(int)

logger.info("Ready to be imported to Database. Altering the features of database")

with engine.connect() as conn:
    logger.info("Clearing the existing data from the table")
    conn.execute(text('TRUNCATE TABLE shows'))
    conn.commit()
    try:
        logger.info("Adding age_rating in numerical format")
        breakpoint()
        conn.execute(text('ALTER TABLE shows ADD age_rating int'))
        conn.commit()
    except:
        logger.error("Column age_rating already exists")
        print("Column already exists")
    else:
        logger.info("Column age_rating added successfully")
        print("Column age added successfully")
    
    try:
        logger.info("Setting show_id as primary key for table shows")
        conn.execute(text('ALTER TABLE shows ADD PRIMARY KEY(show_id)'))
        conn.commit()
    except:
        logger.error("show_id is already set as primary key")
        print("Primary key already exists")
    else:
        logger.info("show_id is set a primary key")
        print("Primary key added")

    try:
        logger.info("show_id is set as a auto_incremental column")
        conn.execute(text('ALTER TABLE shows MODIFY show_id serial'))
        conn.commit()
    except:
        logger.error("Couldn't set show_id as auto_incremental column")
        print("Couldn't update primary key to auto increment")
    else:
        logger.info("Updated show_id to auto_incremental column")
        print("Updated primary key to auto increment")

logger.info("Converting the dataframe to sql table")
shows.to_sql('shows', con=engine, if_exists='append', index=False)
engine.dispose()

logger.info("Importing of .csv file to sql database successful")