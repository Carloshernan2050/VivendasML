import pandas as pd
from sklearn.linear_model import LinearRegression
from tabulate import tabulate
from pymongo import MongoClient

class ViviendaModel:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client['inmobiliaria']
        self.collection = self.db['viviendas']
        self.modelo = None
        self.coeficientes = None
        self.intercepto = None

    def obtener_datos(self):
        documentos = list(self.collection.find({}, {'_id': 0}))
        df = pd.DataFrame(documentos)
        # Asegurar nombres de columnas correctos
        df = df.rename(columns={'Antigüedad': 'antiguedad'})
        df['antiguedad'] = 2025 - df['antiguedad']
        return df[['precio', 'habitaciones', 'area', 'antiguedad', 'fecha_publicacion', 'descripcion']]

    def entrenar_modelo(self):
        datos = self.obtener_datos()
        X = datos[['area', 'antiguedad']]
        y = datos['precio']
        
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        self.modelo = modelo
        self.coeficientes = modelo.coef_
        self.intercepto = modelo.intercept_
        
        return modelo, self.intercepto, self.coeficientes

    def predecir_precio(self, area, antiguedad):
        if self.modelo is None:
            self.entrenar_modelo()
            
        return self.modelo.predict([[area, antiguedad]])[0]

    def mostrar_tabla(self):
        documentos = list(self.collection.find({}, {'_id': 0}))
        print(tabulate(documentos, headers='keys', tablefmt='grid'))