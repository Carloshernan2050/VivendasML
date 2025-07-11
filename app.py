from flask import Flask
from src.controllers.vivienda_controller import vivienda_blueprint

app = Flask(__name__, template_folder='src/templates')
app.register_blueprint(vivienda_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
