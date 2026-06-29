import os

class Config:
    # Clave secreta para proteger las sesiones de las cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clavesecreta123'
    # Nombre estandarizado de nuestro archivo de base de datos
    DATABASE = 'database.db'