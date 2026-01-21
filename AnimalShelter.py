import os
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Using os.getenv allows the app to be secure. 
        # The second string is a fallback for local development only.
        USER = os.getenv('MONGO_USER', 'aacuser')
        PASS = os.getenv('MONGO_PASS', 'password_1')
        HOST = os.getenv('MONGO_HOST', 'nv-desktop-services.apporto.com')
        PORT = os.getenv('MONGO_PORT', '32296')
        DB = os.getenv('MONGO_DB', 'AAC')
        COL = os.getenv('MONGO_COL', 'animals')

        # MongoDB Connection with updated f-string for better readability
        try:
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=admin')
            self.database = self.client[DB]
            self.collection = self.database[COL]
            # Health check: triggers a connection to verify credentials
            self.client.admin.command('ping') 
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def create(self, data):
        """ Inserts a document. Returns True if successful. """
        if data is not None:
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except Exception as e:
                #  I would update a logging library here
                print(f"Insert failed: {e}")
                return False
        else:
            raise ValueError("No data provided to insert.")

    def read(self, query=None):
        """ Queries documents. Defaults to empty query if none provided. """
        try:
            # Using query or {} ensures the method doesn't crash if called without args
            result = list(self.collection.find(query or {}))
            return result
        except Exception as e:
            print(f"Read failed: {e}")
            return []
