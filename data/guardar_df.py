import pandas as pd
from tabulate import tabulate

ruta = 'C:/laragon/www/VivendasML/dataset_vivienda.xlsx'
df = pd.read_excel(ruta, header=None)

print(tabulate(df.head(11), tablefmt='grid'))

df.columns = ['ID', 'Precio', 'Area','Habitaciones','Antigüedad','fecha_publicacion','descripcion']

total_viviendas = len(df)
promedio_precio_m2 = df.groupby('habitaciones')['precio_m2'].mean().reset_index()
