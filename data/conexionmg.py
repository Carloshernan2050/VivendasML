import pandas as pd
from pymongo import MongoClient

def get_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")

    db = client['inmobiliaria']  # Usamos siempre la misma base
    print("✅ Conexión exitosa a MongoDB")
    return db

def cargar_datos_iniciales():
    db = get_mongo_connection()
    coleccion = db['viviendas']
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv('data/dataset_viviendas.csv')
        df = df.dropna()

        # Renombrar columna si tiene acentos
        if 'Antigüedad' in df.columns:
            df = df.rename(columns={'Antigüedad': 'antiguedad'})

        # Convertir a lista de diccionarios e insertar
        datos = df.to_dict(orient='records')
        coleccion.insert_many(datos)

        print(f"✅ {len(datos)} documentos insertados en MongoDB con éxito.")
    except FileNotFoundError:
        print("❌ Archivo CSV no encontrado en: data/dataset_viviendas.csv")
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")