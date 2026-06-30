from flask import Flask
from flask_login import LoginManager
from config import Config
from models import init_db
from routes import configure_routes

# Inicialización de la instancia central de la aplicación web
app = Flask(__name__)
app.config.from_object(Config)

# Configuración del motor de sesiones seguras en el servidor
login_manager = LoginManager()
login_manager.init_app(app)
# Define la ruta de redirección global para accesos no autorizados (@login_required)
login_manager.login_view = 'login'

# Inicialización obligatoria del esquema de persistencia local
init_db()

# Inyección modular de los controladores web de tráfico
configure_routes(app, login_manager)

if __name__ == '__main__':
    # Ejecución en modo depuración local sobre el puerto alternativo de desarrollo
    app.run(debug=True, port=5001)