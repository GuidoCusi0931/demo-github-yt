from flask import Flask, render_template, request
import sqlite3  # <-- 1. Importamos la librería de Base de Datos

app = Flask(__name__)

# 2. Función para conectar a la BD y crear la tabla si no existe
def init_db():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Dejamos los campos TEXT limpios y sencillos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            mensaje TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
