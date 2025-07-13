from flask import Blueprint, render_template, request, flash
from datetime import datetime
from src.models.vivienda_model import ViviendaModel

vivienda_blueprint = Blueprint('vivienda', __name__)
modelo = ViviendaModel()

@vivienda_blueprint.route('/')
def index():
    try:
        datos = modelo.obtener_datos(limite=1000)

        total_viviendas = len(datos)

        # Calcular promedio por metro cuadrado
        precios_m2 = [
            v['precio'] / v['area']
            for v in datos
            if 'precio' in v and 'area' in v and isinstance(v['precio'], (int, float)) and isinstance(v['area'], (int, float)) and v['area'] > 0
        ]
        promedio_m2 = sum(precios_m2) / len(precios_m2) if precios_m2 else 0

        # Clasificación por tipo de vivienda
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
            precio_promedio=promedio_m2,  # <-- este es el nuevo promedio por m2
            current_year=datetime.now().year,
            contador_tipos=contador_tipos
        )
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template(
            'index.html',
            total_viviendas=0,
            precio_promedio=0,
            current_year=datetime.now().year,
            contador_tipos={"Casa": 0, "Apartamento": 0, "Otros": 0}
        )



@vivienda_blueprint.route('/predecir', methods=['POST'])
def predecir():
    try:
        # Validate form data
        area = float(request.form.get('area', 0))
        antiguedad = int(request.form.get('antiguedad', 0))
        
        if area <= 0 or antiguedad < 0:
            flash('Por favor ingrese valores válidos para área y antigüedad', 'error')
            return render_template('index.html')

        # Predict price
        precio_estimado = modelo.predecir_precio(area, antiguedad)
        _, intercepto, coeficientes = modelo.entrenar_modelo()

        return render_template(
            'resultado.html',
            area=area,
            antiguedad=antiguedad,
            precio=round(precio_estimado, 2),
            intercepto=round(intercepto, 2),
            coef_area=round(coeficientes[0], 2),
            coef_antig=round(coeficientes[1], 2)
        )
    except Exception as e:
        print(f"Error in prediction: {e}")
        flash(f'Error en la predicción: {str(e)}', 'error')
        return render_template('index.html')

from dateutil import parser  # solo necesitas instalar python-dateutil si no lo tienes

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

            # 🏗️ Fecha de construcción = fecha_publicacion (como string)
            fecha_pub = doc.get('fecha_publicacion')
            if isinstance(fecha_pub, str):
                try:
                    fecha_dt = parser.parse(fecha_pub)
                    doc['fecha_construccion'] = fecha_dt.strftime('%Y-%m-%d')
                    doc['antiguedad_anos'] = (datetime.now() - fecha_dt).days // 365
                except Exception as e:
                    print(f"⚠️ Fecha inválida: {fecha_pub} ({e})")
                    doc['fecha_construccion'] = 'Desconocida'
                    doc['antiguedad_anos'] = 'Desconocida'
            else:
                doc['fecha_construccion'] = 'Desconocida'
                doc['antiguedad_anos'] = 'Desconocida'

            # 🏠 Clasificar tipo de vivienda
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
        print(f"Error en listar_viviendas: {e}")
        flash(f'Error al cargar el listado: {str(e)}', 'error')
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

            puntos.append({
                "precio": precio,
                "m2": round(precio / area, 2),
                "tipo": tipo
            })

        return render_template("scatter.html", puntos=puntos)
    except Exception as e:
        print(f"Error en /grafico_dispersion: {e}")
        flash("Error al generar el gráfico de dispersión", "danger")
        return render_template("error.html", mensaje=str(e))
