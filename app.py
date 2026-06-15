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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
