from flask import Blueprint, render_template, request
from models.vivienda_model import ViviendaModel

vivienda_blueprint = Blueprint('vivienda', __name__)
modelo = ViviendaModel()

@vivienda_blueprint.route('/')
def index():
    return render_template('index.html')

@vivienda_blueprint.route('/predecir', methods=['POST'])
def predecir():
    try:
        # Capturar datos del formulario
        area = float(request.form['area'])
        antiguedad = int(request.form['antiguedad'])

        # Predecir precio
        precio_estimado = modelo.predecir_precio(area, antiguedad)
        intercepto, coeficientes = modelo.entrenar_modelo()[1:]

        return render_template('resultado.html',
                               area=area,
                               antiguedad=antiguedad,
                               precio=round(precio_estimado, 2),
                               intercepto=round(intercepto, 2),
                               coef_area=round(coeficientes[0], 2),
                               coef_antig=round(coeficientes[1], 2))
    except Exception as e:
        return f"Error en la predicción: {e}"
