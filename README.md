# 🚀 Mi Primer CRUD con Flask y SQLite

¡Bienvenido! Este es un proyecto de práctica backend donde construí una aplicación web interactiva desde cero utilizando **Python**, el microframework **Flask**, y **SQLite** como motor de base de datos. 

La aplicación implementa el ciclo completo de un **CRUD** (Create, Read, Update, Delete) a través de un sistema de gestión de mensajes de contacto.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3** (Lógica del servidor)
* **Flask** (Framework web)
* **Jinja2** (Motor de plantillas HTML dinámicas)
* **SQLite3** (Base de datos relacional local)
* **Git & GitHub** (Control de versiones)

---

## 📋 Características del Proyecto

* **Entorno Virtual (`venv`):** Configurado para mantener las dependencias aisladas de forma limpia.
* **Rutas Dinámicas:** Páginas de Inicio, Perfil de usuario, Formulario de Contacto, Visualización y Edición.
* **Persistencia de Datos:** Creación automática de la base de datos (`database.db`) e inserción segura de registros para evitar inyecciones SQL.
* **Ciclo CRUD Completo:**
    * **C (Create):** Envío de datos mediante formulario web con el método `POST`.
    * **R (Read):** Extracción de datos con `SELECT` y renderizado en una tabla HTML.
    * **U (Update):** Modificación de registros existentes mediante formularios precargados y el comando `UPDATE`.
    * **D (Delete):** Eliminación de registros con confirmación previa en el navegador utilizando `DELETE FROM`.
* **Compatibilidad con macOS:** Configuración adaptada al puerto `5001` para evitar conflictos con el receptor AirPlay nativo de Mac.

---

## 💻 Cómo Ejecutar el Proyecto Localmente

Sigue estos pasos para clonar y arrancar la aplicación en tu computadora:

### 1. Clonar el repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO_DE_GITHUB>
cd "demo github yt"