from pymongo import MongoClient
import csv
import os

def get_database():
    client = MongoClient("localhost", 27017)
    db = client.netflix
    return db

if __name__ == '__main__':
    db = get_database()
    curr_directory = os.getcwd()
    curr_directory = curr_directory.replace("\\", "\\\\")

    data = open(curr_directory + '\\data\\netflix_titles.csv', encoding='utf-8')
    csv_data = csv.reader(data)
    data_lines = list(csv_data)
    for x in data_lines[1:]:
        x[0] = int(x[0][1:])
        x[7] = int(x[7])
        data_df = {'show_id': x[0], 'type': x[1],'title': x[2],'director': x[3],'cast': x[4],
            'country': x[5],'date_added': x[6],'release_year': x[7], 'rating': x[8],
            'duration': x[9],'listed_in': x[10], 'description': x[11]}
        db.shows.insert_one(data_df)