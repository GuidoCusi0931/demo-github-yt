from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
import sqlite3  # <-- 1. Importamos la librería de Base de Datos

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clavesecreta123' 

login_manager = LoginManager()
login_manager.init_app(app)
# Esto le dice a Flask-Login a dónde mandar al usuario si intenta entrar a una ruta protegida sin loguearse:
login_manager.login_view = 'login'

def init_db():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    
    # Tabla de mensajes (la que ya tenías)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            mensaje TEXT
        )
    ''')
    
    # NUEVA: Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conexion.commit()
    conexion.close()

# El molde que exige Flask-Login
class Usuario(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

# El cargador que busca al usuario en la BD usando el ID de la cookie
@login_manager.user_loader
def load_user(user_id):
    conexion = sqlite3.connect('database.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    user_row = cursor.fetchone()
    conexion.close()
    
    if user_row:
        return Usuario(id=user_row['id'], email=user_row['email'])
    return None

# Ejecutamos la función para que la BD se cree al arrancar la app
init_db()


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', usuario="Guido", rol="Desarrollador Backend")


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    mensaje_exito = None
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre')
        texto_mensaje = request.form.get('mensaje')
        
        # 3. GUARDAR EN LA BASE DE DATOS (Usamos INSERT)
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()
        
        # Los signos '?' son por seguridad, para evitar hackeos (SQL Injection)
        cursor.execute('''
            INSERT INTO mensajes (nombre, mensaje) 
            VALUES (?, ?)
        ''', (nombre_usuario, texto_mensaje))
        
        conexion.commit()  # Guarda los cambios de verdad
        conexion.close()   # Cierra la conexión siempre
        
        mensaje_exito = f"¡Gracias {nombre_usuario}! Tu mensaje fue guardado en la Base de Datos."

    return render_template('contacto.html', mensaje_exito=mensaje_exito)

@app.route('/mensajes')
@login_required # <-- ¡ESTE ES EL CANDADO!
def ver_mensajes():
    # 1. Nos conectamos a la base de datos
    conexion = sqlite3.connect('database.db')
    # Cambiamos el formato de salida para que sea más fácil de leer en el HTML (como un diccionario)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    # 2. Traemos todos los registros de la tabla mensajes
    cursor.execute('SELECT * FROM mensajes')
    todos_los_mensajes = cursor.fetchall()  # Captura todas las filas
    
    conexion.close()
    
    # 3. Le pasamos esos mensajes al nuevo archivo HTML
    return render_template('ver_mensajes.html', lista_mensajes=todos_los_mensajes)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required # <-- ¡ESTE ES EL CANDADO!
def editar_mensaje(id):
    conexion = sqlite3.connect('database.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    # Si el usuario entra a la página (GET), buscamos el mensaje actual para rellenar el formulario
    if request.method == 'GET':
        cursor.execute('SELECT * FROM mensajes WHERE id = ?', (id,))
        mensaje = cursor.fetchone()
        conexion.close()
        
        # Si el ID no existe en la BD, volvemos a la lista
        if mensaje is None:
            return "Mensaje no encontrado", 404
            
        return render_template('editar_mensaje.html', mensaje=mensaje)

    # Si el usuario envía el formulario con los cambios (POST)
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nuevo_texto = request.form.get('mensaje')

        # El comando UPDATE modifica los campos filtrando por el ID
        cursor.execute('''
            UPDATE mensajes 
            SET nombre = ?, mensaje = ? 
            WHERE id = ?
        ''', (nuevo_nombre, nuevo_texto, id))
        
        conexion.commit()
        conexion.close()

        # Al terminar, redirigimos al usuario de vuelta a la lista de mensajes
        from flask import redirect, url_for
        return redirect(url_for('ver_mensajes'))

@app.route('/eliminar/<int:id>')
@login_required # <-- ¡ESTE ES EL CANDADO!
def eliminar_mensaje(id):
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    
    # El comando DELETE borra la fila que coincida con el ID
    cursor.execute('DELETE FROM mensajes WHERE id = ?', (id,))
    
    conexion.commit()
    conexion.close()
    
    # Redirigimos de inmediato a la lista para ver el cambio
    from flask import redirect, url_for
    return redirect(url_for('ver_mensajes'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Encriptamos la contraseña antes de guardarla
        password_encriptada = generate_password_hash(password)
        
        try:
            conexion = sqlite3.connect('database.db')
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO usuarios (email, password) VALUES (?, ?)', (email, password_encriptada))
            conexion.commit()
            conexion.close()
            return "¡Usuario registrado con éxito! Ya puedes ir a /login"
        except sqlite3.IntegrityError:
            return "Ese email ya está registrado."
            
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conexion = sqlite3.connect('database.db')
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario_db = cursor.fetchone()
        conexion.close()
        
        # Si el usuario existe y la contraseña coincide con el hash
        if usuario_db and check_password_hash(usuario_db['password'], password):
            # Creamos el objeto de usuario y le damos la sesión activa
            usuario_objeto = Usuario(id=usuario_db['id'], email=usuario_db['email'])
            login_user(usuario_objeto)
            return redirect(url_for('ver_mensajes'))
        else:
            return "Credenciales incorrectas, vuelve a intentarlo."
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() # Rompe la sesión segura
    # En lugar de devolver texto plano viejo, redirigimos al login
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
