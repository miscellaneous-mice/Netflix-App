import csv
import os
from sqlalchemy import text
from create_sql_db import Shows, SessionLocal, ShowsVerify

session = SessionLocal()

print("\nReading a csv file")

curr_directory = os.getcwd()
curr_directory = curr_directory.replace("\\", "\\\\")

data = open(curr_directory + '\\data\\netflix_titles.csv', encoding='utf-8')
csv_data = csv.reader(data)
data_lines = list(csv_data)

print(len(data_lines))
print(data_lines[0]) # Table of contents
print(data_lines[1])

session.execute(text('TRUNCATE TABLE data'))

try:
    session.execute(text('ALTER TABLE data ADD PRIMARY KEY(show_id)'))
except:
    print("Primary key already exists")
else:
    print("Primary key added")

try:
    session.execute(text('ALTER TABLE data MODIFY show_id INT AUTO_INCREMENT'))
except:
    print("Couldn't update primary key to auto increment")
else:
    print("Updated primary key to auto increment")

for x in data_lines[1:]:
    x[0] = int(x[0][1:])
    x[7] = int(x[7])
    data_df = {'type': x[1],'title': x[2],'director': x[3],'cast': x[4],
           'country': x[5],'date_added': x[6],'release_year': x[7], 'rating': x[8],
           'duration': x[9],'listed_in': x[10], 'description': x[11]}
    shows_request = ShowsVerify(**data_df)
    show = Shows(**shows_request.model_dump())
    session.add(show)
    session.commit()

data.close()
session.close()