

# Servidor corriendo en el entorno virtual
![uvicorn](image-3.png)

# Capturas Swagger UI

## Get Users
![get users](image-1.png)

## Get users-id
![Get users id](image.png)

## Post users
![Post users](image-2.png)

### Reflexion personal FastApi 
El desarrollo del proyecto device_systems demostró que FastAPI optimiza drásticamente los tiempos de desarrollo al unificar el tipado estático de Python con el protocolo HTTP. Gracias a su integración nativa con Pydantic v2, el framework gestiona de forma automática la validación estricta de datos (como correos y roles) y el control de respuestas mediante Response Models, reduciendo las líneas de código manual. Además, herramientas automatizadas como Swagger UI facilitan las pruebas en tiempo real de la lógica de negocio —como el control de duplicados (400) o filtrados— e inyectar cabeceras personalizadas de manera limpia, logrando una API robusta, estandarizada y altamente escalable con el mínimo esfuerzo.
