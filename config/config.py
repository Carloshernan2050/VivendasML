import os
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError


load_dotenv()

class MongoConfig:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("DB_NAME", "inmobiliaria")
        self.collection_name = os.getenv("COLLECTION_NAME", "viviendas")

        if not self.URL:
            raise ConfigurationError("MongoDB URI no esta configurado")
        
        if not self.URL.startswith('mongodb://', 'mongodb+srv://'):
            raise ConfigurationError("Formato de URL MongoDB invalido")

class AppConfig:
    def __init__(self):
        self.Mongo = MongoConfig()
        self.Debug = os.getenv('DEBUG', 'False').lower() == 'true'

config = AppConfig() 