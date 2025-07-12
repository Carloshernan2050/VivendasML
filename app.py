import os
import sys
from pathlib import Path
from flask import Flask

BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

from core.config import config

def create_app():
    app = Flask(__name__)
    app.config.update({
        'DEBUG': config.debug,
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-123')
    })

    # Registrar blueprints
    from src.controllers.vivienda_controller import vivienda_blueprint
    app.register_blueprint(vivienda_blueprint)

    # Conexión a MongoDB (nuevo enfoque para Flask 2.3+)
    @app.before_request
    def init_db():
        from core.database import MongoDBConnection
        if not hasattr(app, 'mongo_initialized'):
            MongoDBConnection()  # Establece conexión
            app.mongo_initialized = True

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.debug)