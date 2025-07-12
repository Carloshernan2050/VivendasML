from flask import Blueprint, render_template, request, flash
from datetime import datetime
from src.models.vivienda_model import ViviendaModel

vivienda_blueprint = Blueprint('vivienda', __name__)
modelo = ViviendaModel()

@vivienda_blueprint.route('/')
def index():
    try:
        # Get basic statistics for the dashboard
        datos = modelo.obtener_datos(limite=1000)  # Limit to 1000 records for performance
        
        # Calculate statistics
        total_viviendas = len(datos)
        precios = [v['precio'] for v in datos if 'precio' in v and isinstance(v['precio'], (int, float))]
        precio_promedio = sum(precios)/len(precios) if precios else 0
        
        return render_template(
            'index.html',
            total_viviendas=total_viviendas,
            precio_promedio=precio_promedio,
            current_year=datetime.now().year
        )
    except Exception as e:
        print(f"Error in index route: {e}")
        # Fallback with default values if there's an error
        return render_template(
            'index.html',
            total_viviendas=0,
            precio_promedio=0,
            current_year=datetime.now().year
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

@vivienda_blueprint.route('/listado')
def listar_viviendas():
    try:
        print("\n=== INICIO DE LISTAR VIVIENDAS ===")
        datos = modelo.obtener_datos()
        
        # Transform data for display
        viviendas = []
        current_year = datetime.now().year
        for doc in datos:
            # Ensure all required fields exist
            doc.setdefault('precio', 0)
            doc.setdefault('area', 0)
            doc.setdefault('habitaciones', 0)
            doc.setdefault('antiguedad', current_year)
            doc.setdefault('descripcion', 'Sin descripción')
            
            # Calculate property age
            doc['antiguedad_anos'] = current_year - doc['antiguedad']
            viviendas.append(doc)
        
        print(f"Datos recibidos del modelo: {len(viviendas)} registros")
        return render_template('mostrar_datos.html', viviendas=viviendas)
    except Exception as e:
        print(f"Error en listar_viviendas: {e}")
        flash(f'Error al cargar el listado: {str(e)}', 'error')
        return render_template('error.html', mensaje=str(e))