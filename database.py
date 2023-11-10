# database.py
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI')
MONGO_NAME = os.environ.get('MONGO_NAME', 'your_default_mongo_name')

class Database:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.get_database(MONGO_NAME)

        # Example: Create a users collection
        self.users_collection = self.db.users

    def add_user(self, user_id):
        # Add a user to the users collection
        user_data = {'user_id': user_id, 'subscribed': False}
        self.users_collection.insert_one(user_data)

    def get_user(self, user_id):
        # Retrieve a user from the users collection
        return self.users_collection.find_one({'user_id': user_id})

    def subscribe_user(self, user_id):
        # Subscribe a user
        self.users_collection.update_one({'user_id': user_id}, {'$set': {'subscribed': True}})

    # Add more methods based on your requirements

# Example usage:
if __name__ == '__main__':
    db = Database()

    # Add a user
    db.add_user(123)

    # Get user data
    user_data = db.get_user(123)
    print(user_data)

    # Subscribe user
    db.subscribe_user(123)
    user_data = db.get_user(123)
    print(user_data)
