from flask import Flask, render_template, request  # <-- ¡Agregamos 'request' aquí!

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', usuario="Guido", rol="Desarrollador Backend")

# <-- Modificamos esta ruta para aceptar GET y POST
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    mensaje_exito = None  # Por defecto no hay mensaje
    
    if request.method == 'POST':
        # Capturamos lo que el usuario escribió usando el atributo 'name' del HTML
        nombre_usuario = request.form.get('nombre')
        texto_mensaje = request.form.get('mensaje')
        
        # Creamos un mensaje para confirmar que recibimos los datos
        mensaje_exito = f"¡Gracias {nombre_usuario}! Hemos recibido tu mensaje: '{texto_mensaje}'"

    # Le pasamos el mensaje_exito a Jinja2
    return render_template('contacto.html', mensaje_exito=mensaje_exito)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # <-- Le decimos que use el puerto 5001