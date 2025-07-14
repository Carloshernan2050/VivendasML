from flask import Blueprint, render_template, request, flash
from datetime import datetime
from dateutil import parser
from src.models.vivienda_model import ViviendaModel

vivienda_blueprint = Blueprint('vivienda', __name__)
modelo = ViviendaModel()

@vivienda_blueprint.route('/')
def index():
    try:
        datos = modelo.obtener_datos(limite=1000)
        total_viviendas = len(datos)

        precios_m2 = [
            v['precio'] / v['area']
            for v in datos
            if 'precio' in v and 'area' in v and isinstance(v['precio'], (int, float)) and isinstance(v['area'], (int, float)) and v['area'] > 0
        ]
        promedio_m2 = sum(precios_m2) / len(precios_m2) if precios_m2 else 0

        contador_tipos = {"Casa": 0, "Apartamento": 0, "Otros": 0}
        for v in datos:
            desc = v.get("descripcion", "").lower()
            if "casa" in desc:
                contador_tipos["Casa"] += 1
            elif "apartamento" in desc:
                contador_tipos["Apartamento"] += 1
            else:
                contador_tipos["Otros"] += 1

        return render_template(
            'index.html',
            total_viviendas=total_viviendas,
            precio_promedio=promedio_m2,
            current_year=datetime.now().year,
            contador_tipos=contador_tipos
        )
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

@vivienda_blueprint.route('/listado')
def listar_viviendas():
    try:
        datos = modelo.obtener_datos()
        viviendas = []

        for doc in datos:
            doc.setdefault('precio', 0)
            doc.setdefault('area', 0)
            doc.setdefault('habitaciones', 0)
            doc.setdefault('descripcion', 'Sin descripción')

            fecha_pub = doc.get('fecha_publicacion')
            if isinstance(fecha_pub, str):
                try:
                    fecha_dt = parser.parse(fecha_pub)
                    doc['fecha_construccion'] = fecha_dt.strftime('%Y-%m-%d')
                    doc['antiguedad_anos'] = (datetime.now() - fecha_dt).days // 365
                except:
                    doc['fecha_construccion'] = 'Desconocida'
                    doc['antiguedad_anos'] = 'Desconocida'

            desc = doc['descripcion'].lower()
            if 'casa' in desc:
                doc['tipo_vivienda'] = 'Casa'
            elif 'apartamento' in desc:
                doc['tipo_vivienda'] = 'Apartamento'
            else:
                doc['tipo_vivienda'] = 'Otros'

            viviendas.append(doc)

        return render_template('mostrar_datos.html', viviendas=viviendas, current_year=datetime.now().year)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

@vivienda_blueprint.route('/grafico_dispersion')
def grafico_dispersion():
    try:
        datos = modelo.obtener_datos()
        puntos = []

        for v in datos:
            precio = v.get("precio")
            area = v.get("area")
            desc = v.get("descripcion", "").lower()

            if not isinstance(precio, (int, float)) or not isinstance(area, (int, float)) or area <= 0:
                continue

            tipo = "Otros"
            if "casa" in desc:
                tipo = "Casa"
            elif "apartamento" in desc:
                tipo = "Apartamento"

            m2 = round(precio / area, 2)
            puntos.append({"precio": precio, "m2": m2, "tipo": tipo})

        return render_template("scatter.html", puntos=puntos)
    except Exception as e:
        return render_template("error.html", mensaje=str(e))
