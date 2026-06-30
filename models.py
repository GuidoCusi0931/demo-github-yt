from flask_login import UserMixin
import sqlite3

# El molde que exige Flask-Login para manejar las sesiones activas
class Usuario(UserMixin):
    """
    Molde de usuario que extiende UserMixin para integrarse con Flask-Login.
    Permite gestionar propiedades como is_authenticated e is_active de forma nativa.
    """
    def __init__(self, id, email):
        self.id = id
        self.email = email

def init_db():
    """
    Inicializa la base de datos SQLite3 de forma síncrona.
    Crea las tablas de 'mensajes' y 'usuarios' con restricciones de integridad si no existen.
    """
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    
    # Tabla de mensajes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            mensaje TEXT
        )
    ''')
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conexion.commit()
    conexion.close()