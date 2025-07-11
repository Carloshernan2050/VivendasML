import pandas as pd
from pymongo import MongoClient

def get_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['viviendas']
    return db

def cargar_datos_iniciales():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['inmobiliaria']
    coleccion = db['viviendas']
    
    # Cargar CSV
    df = pd.read_csv('data/dataset_viviendas.csv')
    df = df.dropna()
    
    # Convertir a diccionario y subir a Mongo
    datos = df.to_dict(orient='records')
    coleccion.insert_many(datos)
    
    print("Datos insertados en MongoDB con éxito.")