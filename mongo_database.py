from pymongo import MongoClient
from functools import cache

@cache
def get_database():
   client = MongoClient("localhost", 27017)
   
   # Getting our database
   db = client.shows

   return db


db = get_database()

# Adding many elements to history collection of shows database
"""
db.history.insert_many([
{"user_id": 1, "watch_history": [{"1" : "22-04-2021"}, {"5": "17-06-2019"}]},
{"user_id": 2, "watch_history": [{"2" : "30-08-2018"}, {"4": "19-01-2024"}]}
])
"""
# Adding one element to history collection of shows database
"""
db.history.insert_one(
{"user_id": 1, "watch_history": [{"2" : "24-02-2018", "4": "14-07-2022"}]}
)
"""

# Finding the element from history collection of shows database
# print(db.history.find_one({"user_id": 1}))

# Updating/ appending an value to an element from history collection of shows database
"""
db.history.update_one({"user_id": 2}, {"$push": {"watch_history" : {"3": "06-07-2023"}}})
"""

def find_history(user_id):
   return db.history.find_one({"user_id": user_id})

def add_history(user_id, show_id, watch_date):
    user_exists = db.history.find_one({"user_id": user_id})
    if user_exists is None:
        db.history.insert_one({"user_id": user_id, "watch_history": [{str(show_id): watch_date}]})
    else:
        db.history.update_one({"user_id": user_id}, {"$push": {"watch_history" : {str(show_id): watch_date}}})
