from flask import Flask

app = Flask(__name__)

# 1. Ruta Principal (Inicio)
@app.route('/')
def inicio():
    return '''
        <h1>🏠 Bienvenido a mi sitio web</h1>
        <p>Esta es la página de inicio creada con Flask.</p>
        <hr>
        <a href="/perfil">Ir al Perfil</a> | <a href="/contacto">Ir a Contacto</a>
    '''

# 2. Segunda Ruta: Perfil
@app.route('/perfil')
def perfil():
    return '''
        <h1>👤 Perfil del Usuario</h1>
        <p>Nombre: Guido Ezequiel Cusi</p>
        <p>Rol: Desarrollador Backend en proceso 🚀</p>
        <hr>
        <a href="/">Volver al Inicio</a>
    '''

# 3. Tercera Ruta: Contacto
@app.route('/contacto')
def contacto():
    return '''
        <h1>📞 Sección de Contacto</h1>
        <p>Puedes escribirme a: guido.ezequiel0931@gmail.com</p>
        <p>O seguirme en mi GitHub.</p>
        <hr>
        <a href="/">Volver al Inicio</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)