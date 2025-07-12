from core.database import MongoDBConnection
from pymongo.errors import PyMongoError
from datetime import datetime

class ViviendaModel:
    def __init__(self):
        self._init_db_connection()

    def _init_db_connection(self):
        """Inicializa la conexión a la base de datos"""
        try:
            self.db_connection = MongoDBConnection()
            self.collection = self.db_connection.get_collection()
            # Validación de conexión
            if self.collection.count_documents({}) >= 0:
                print(f"✅ Modelo conectado a colección: {self.collection.name}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            raise

    def obtener_datos(self, filtro=None, campos=None, limite=0):
        """
        Obtiene datos de viviendas con opciones avanzadas
        
        Args:
            filtro (dict): Filtros de búsqueda
            campos (dict): Campos a incluir/excluir (1 incluir, 0 excluir)
            limite (int): Límite de resultados (0 = sin límite)
        """
        try:
            # Configuración por defecto
            filtro = filtro or {}
            campos = campos or {"_id": 0}
            
            cursor = self.collection.find(filtro, campos)
            if limite > 0:
                cursor = cursor.limit(limite)
                
            datos = list(cursor)
            self._log_datos(datos)
            return self._transformar_datos(datos)
            
        except PyMongoError as e:
            self._log_error(e)
            return []

    def _transformar_datos(self, datos):
        """Transforma los datos antes de devolverlos"""
        current_year = datetime.now().year
        for doc in datos:
            # Calcular años de antigüedad
            if 'antiguedad' in doc and isinstance(doc['antiguedad'], int):
                doc['antiguedad_anos'] = current_year - doc['antiguedad']
            # Formatear precio
            if 'precio' in doc:
                doc['precio_formateado'] = f"${doc['precio']:,.0f}"
        return datos

    def _log_datos(self, datos):
        """Registro de depuración"""
        print(f"\n📦 Datos obtenidos ({len(datos)} registros)")
        if datos and len(datos) > 0:
            print("📄 Ejemplo:", {k: v for k, v in datos[0].items() if k != '_id'})

    def _log_error(self, error):
        """Manejo centralizado de errores"""
        print(f"🔥 Error MongoDB [{type(error).__name__}]: {error}")