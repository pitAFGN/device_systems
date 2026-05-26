# Device Systems - API REST de Usuarios

## 📝 Descripción
`device_systems` es una API REST funcional desarrollada con **FastAPI** y **Pydantic v2** diseñada para administrar de manera estructurada los usuarios del sistema. El proyecto implementa validaciones estrictas de datos de entrada, manejo de parámetros de ruta y consulta, prevención de registros duplicados en memoria y respuestas HTTP estandarizadas con cabeceras personalizadas.

---

## 🚀 Instalación y Ejecución

Sigue estos comandos básicos en tu terminal para configurar el entorno virtual y ejecutar el servidor:

### 1. Crear y Activar el Entorno Virtual
Abre una terminal en la raíz de la carpeta `device_systems`:

* **En Windows (CMD / PowerShell):**
  ```bash
  python -m nombre_proyecto venv
 nombre_proyecto\Scripts\activate

  pip install -r requirements.txt

  uvicorn app.main:app --reload

  Direcciones de Acceso
Una vez levantado el servidor, puedes ingresar desde tu navegador a las siguientes URLs:

Servidor Base de la API: http://127.0.0.1:8000

Documentación Interactiva (Swagger UI): http://127.0.0.1:8000/docs