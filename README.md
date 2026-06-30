# 📱 Sistema Seguro de Registro y Mensajería Backend

Aplicación web modular desarrollada en Python con el framework **Flask**, persistencia de datos en **SQLite3**, seguridad criptográfica para autenticación de usuarios y maquetación adaptable mediante **Bootstrap 5**.

🚀 **[VER DEMO EN VIVO EN RENDER](https://sistema-mensajes-guido.onrender.com)** *(Nota: Al usar un plan gratuito en Render, el servidor puede demorar unos 50 segundos en arrancar si estuvo inactivo).*

---

## 🛠️ Características Principales

* **Autenticación Segura:** Registro e Inicio de sesión protegido mediante hashing de contraseñas con la librería `Werkzeug` y gestión de estados de sesión con `Flask-Login`.
* **Operaciones CRUD Completas:** Panel privado para crear, leer, actualizar y eliminar mensajes directamente de la base de datos relacional.
* **Arquitectura Modular:** Separación de responsabilidades limpia dividida en controladores de rutas, esquemas de datos y archivos de configuración.
* **Interfaz Responsive:** Diseño adaptado a dispositivos móviles utilizando el sistema de rejillas y contenedores de Bootstrap 5.

---

## 📁 Estructura del Proyecto (Arquitectura Modular)

El código se encuentra organizado bajo el principio de separación de responsabilidades:

* `app.py`: Punto de entrada e inicialización central del servidor y plugins.
* `config.py`: Centralización de variables de entorno y claves criptográficas (`SECRET_KEY`).
* `models.py`: Estructura y esquemas de las tablas de la base de datos (`usuarios` y `mensajes`).
* `routes.py`: Controladores de tráfico web y lógica de negocio para cada endpoint de la app.
* `templates/`: Capa de presentación (HTML + Jinja2) que hereda de un diseño global (`base.html`).

---

## 💻 Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Framework Web:** Flask
* **Base de Datos:** SQLite3
* **Seguridad:** Werkzeug (Password Hashing) & Flask-Login (Session Management)
* **Frontend:** HTML5, Jinja2 y Bootstrap 5

---

## 🚀 Instalación y Ejecución Local

1. Clonar el repositorio.
2. Crear un entorno virtual: `python3 -m venv venv` e iniciarlo.
3. Instalar las dependencias requeridas: `pip install -r requirements.txt`
4. Ejecutar la aplicación: `python3 app.py` (Acceder localmente en `http://localhost:5001`).