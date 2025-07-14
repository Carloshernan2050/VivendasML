from flask import Blueprint, render_template
from sklearn.linear_model import LinearRegression
import numpy as np
from src.models.vivienda_model import ViviendaModel

analisis_blueprint = Blueprint('analisis', __name__)
modelo = ViviendaModel()

@analisis_blueprint.route('/grafico_regresion')
def grafico_regresion():
    try:
        datos = modelo.obtener_datos()
        puntos = []
        precios = []
        valores_m2 = []

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
            precios.append(precio)
            valores_m2.append(m2)

        modelo_rl = LinearRegression().fit(np.array(precios).reshape(-1, 1), np.array(valores_m2))
        pendiente = modelo_rl.coef_[0]
        intercepto = modelo_rl.intercept_

        min_x = min(precios)
        max_x = max(precios)
        min_y = pendiente * min_x + intercepto
        max_y = pendiente * max_x + intercepto

        return render_template(
            "grafico_regresion.html",
            puntos=puntos,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            total_viviendas=len(puntos)
        )

    except Exception as e:
        return render_template("error.html", mensaje=str(e))
