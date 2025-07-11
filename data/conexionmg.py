from pymongo import MongoClient
from .config import config

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(config.MONGO.URL)
            cls._instance.db = cls._instance.client[config.MONGO.DB_NAME]
        return cls._instance
    
    def get_collection(self, collection_name=None):
        return self.db[collection_name or config.MONGO.COLLECTION]