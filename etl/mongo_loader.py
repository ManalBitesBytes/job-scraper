from pymongo import MongoClient

class MongoLoader(object):
    def __init__(self, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
        # Connect to MongoDB
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]  # Database
        self.collection = self.db[collection_name]  # Collection


    def load(self, data):
        if data:
            # Insert the data into MongoDB collection
            # Use insert_many to insert multiple records at once
            self.collection.insert_many(data)
            print(f"{len(data)} records inserted into MongoDB")
        else:
            print("No data to insert.")
