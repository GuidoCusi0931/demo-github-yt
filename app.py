from flask import Flask
from flask_login import LoginManager
from config import Config
from models import init_db
from routes import configure_routes

# 1. Instanciamos la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# 2. Inicializamos el gestor de sesiones de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 3. Inicializamos las tablas de la base de datos al arrancar
init_db()

# 4. Inyectamos las rutas de forma modular en nuestra app
configure_routes(app, login_manager)

if __name__ == '__main__':
    # Configurado en puerto 5001 para coincidir con tu entorno de desarrollo local
    app.run(debug=True, port=5001)