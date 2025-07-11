import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
COLLECTION_NAME_2 = os.getenv('COLLECTION_NAME_2')
DATASET_NAME = os.getenv('DATASET_NAME')

