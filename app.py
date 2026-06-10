from flask import Flask, render_template  # <-- Importamos render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    # Buscará el archivo 'inicio.html' dentro de la carpeta 'templates'
    return render_template('inicio.html')

@app.route('/perfil')
def perfil():
    # Pasamos variables desde Python hacia el HTML de Jinja2
    return render_template('perfil.html', usuario="Guido", rol="Desarrollador Backend")

@app.route('/contacto')
def contacto():
    return render_template('contacto.html', email="guido.ezequiel0931@gmail.com")

if __name__ == '__main__':
    app.run(debug=True)