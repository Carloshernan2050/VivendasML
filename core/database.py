from pymongo import MongoClient
from .config import config

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.client = MongoClient(
                    config.mongo.url,
                    connectTimeoutMS=3000,
                    serverSelectionTimeoutMS=3000
                )
                # Test connection
                cls._instance.client.server_info()
                cls._instance.db = cls._instance.client[config.mongo.db_name]
                print("✅ Conexión a MongoDB establecida")
            except Exception as e:
                print(f"❌ Error conectando a MongoDB: {e}")
                raise
        return cls._instance
    
    def get_collection(self, name=None):
        return self.db[name or config.mongo.collection]