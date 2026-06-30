import os

class Config:
    '''Configuracion base para el entorno de produccion y desarrollo'''

    # Clave criptográfica para asegurar las cookies de sesión de Flask-Login
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clavesecreta123'

    # Nombre y extensión del archivo de base de datos relacional
    DATABASE = 'database.db'