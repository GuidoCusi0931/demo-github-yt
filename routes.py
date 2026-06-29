from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import Usuario

def configure_routes(app, login_manager):
    """Registra todas las rutas web en la instancia central de la aplicación."""

    @login_manager.user_loader
    def load_user(user_id):
        conexion = sqlite3.connect(app.config['DATABASE'])
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
        user_row = cursor.fetchone()
        conexion.close()
        
        if user_row:
            return Usuario(id=user_row['id'], email=user_row['email'])
        return None

    @app.route('/')
    def inicio():
        return render_template('inicio.html')

    @app.route('/perfil')
    @login_required
    def perfil():
        return render_template('perfil.html')

    @app.route('/contacto', methods=['GET', 'POST'])
    def contacto():
        mensaje_exito = None
        if request.method == 'POST':
            nombre_usuario = request.form.get('nombre')
            texto_mensaje = request.form.get('mensaje')
            
            conexion = sqlite3.connect(app.config['DATABASE'])
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO mensajes (nombre, mensaje) VALUES (?, ?)', (nombre_usuario, texto_mensaje))
            conexion.commit()
            conexion.close()
            
            mensaje_exito = f"¡Gracias {nombre_usuario}! Tu mensaje fue guardado."
        return render_template('contacto.html', mensaje_exito=mensaje_exito)

    @app.route('/mensajes')
    @login_required
    def ver_mensajes():
        conexion = sqlite3.connect(app.config['DATABASE'])
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM mensajes')
        todos_los_mensajes = cursor.fetchall()
        conexion.close()
        return render_template('ver_mensajes.html', lista_mensajes=todos_los_mensajes)

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    @login_required
    def editar_mensaje(id):
        conexion = sqlite3.connect(app.config['DATABASE'])
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        if request.method == 'GET':
            cursor.execute('SELECT * FROM mensajes WHERE id = ?', (id,))
            mensaje = cursor.fetchone()
            conexion.close()
            if mensaje is None:
                return "Mensaje no encontrado", 404
            return render_template('editar_mensaje.html', mensaje=mensaje)

        if request.method == 'POST':
            nuevo_nombre = request.form.get('nombre')
            nuevo_texto = request.form.get('mensaje')
            cursor.execute('UPDATE mensajes SET nombre = ?, mensaje = ? WHERE id = ?', (nuevo_nombre, nuevo_texto, id))
            conexion.commit()
            conexion.close()
            return redirect(url_for('ver_mensajes'))

    @app.route('/eliminar/<int:id>')
    @login_required
    def eliminar_mensaje(id):
        conexion = sqlite3.connect(app.config['DATABASE'])
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM mensajes WHERE id = ?', (id,))
        conexion.commit()
        conexion.close()
        return redirect(url_for('ver_mensajes'))

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            password_encriptada = generate_password_hash(password)
            
            try:
                conexion = sqlite3.connect(app.config['DATABASE'])
                cursor = conexion.cursor()
                cursor.execute('INSERT INTO usuarios (email, password) VALUES (?, ?)', (email, password_encriptada))
                conexion.commit()
                conexion.close()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Ese email ya está registrado."
        return render_template('registro.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            conexion = sqlite3.connect(app.config['DATABASE'])
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            usuario_db = cursor.fetchone()
            conexion.close()
            
            if usuario_db and check_password_hash(usuario_db['password'], password):
                usuario_objeto = Usuario(id=usuario_db['id'], email=usuario_db['email'])
                login_user(usuario_objeto)
                return redirect(url_for('ver_mensajes'))
            else:
                return "Credenciales incorrectas, vuelve a intentarlo."
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))