import os
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError

load_dotenv()

class MongoConfig:
    def __init__(self):
        # Usamos get() para manejar valores nulos
        self.url = os.getenv('MONGO_URL') or 'mongodb://localhost:27017/'
        self.db_name = os.getenv('MONGO_DB') or 'inmobiliaria'
        self.collection = os.getenv('MONGO_COLLECTION') or 'viviendas'
        
        if not self.url.startswith(('mongodb://', 'mongodb+srv://')):
            raise ConfigurationError("Formato de URL MongoDB inválido")

class AppConfig:
    def __init__(self):
        self.mongo = MongoConfig()
        self.debug = os.getenv('DEBUG', 'True').lower() == 'true'

# Instancia única de configuración
config = AppConfig()