Secuelas - Plataforma de Aprendizaje SQL Interactivo
Este proyecto es una aplicación web interactiva diseñada para enseñar SQL a través de una serie de misiones narrativas. La aplicación se ha estructurado utilizando una arquitectura de microservicios moderna, separando el frontend (React) del backend (Flask).

Arquitectura del Proyecto
El proyecto está compuesto por los siguientes directorios y servicios:

backend/: Contiene la API de Flask escrita en Python. Se encarga de la lógica del juego, la gestión de misiones, la ejecución de consultas SQL y la interacción con la base de datos.

frontend/: Contiene la aplicación de React escrita en TypeScript. Proporciona la interfaz de usuario (la terminal del analista) y se comunica con la API del backend para obtener el estado del juego y enviar las acciones del usuario.

docker-compose.yml: Archivo de orquestación que define y ejecuta todos los servicios de la aplicación (backend, frontend y administrador de base de datos).

README.md: Este archivo.

Servicios
Backend (Flask): Se ejecuta en el puerto 5001.

Frontend (React): Se ejecuta en el puerto 3000.

Adminer (Database Admin): Se ejecuta en el puerto 8080.

Cómo Ejecutar el Proyecto
Prerrequisitos
Docker y Docker Compose deben estar instalados en su sistema.

Pasos para la Instalación y Ejecución
Clonar el Repositorio
Si está trabajando desde un repositorio de git, clónelo. De lo contrario, asegúrese de tener todos los archivos en la estructura de directorios correcta.

Construir y Ejecutar los Contenedores
Abra una terminal en el directorio raíz del proyecto (Secuelas/) y ejecute el siguiente comando:

docker-compose up --build

--build: Este flag le indica a Docker Compose que construya las imágenes de los contenedores desde los Dockerfile antes de iniciarlos. Solo es necesario la primera vez o cuando realice cambios en los Dockerfile o en los archivos de dependencias (requirements.txt, package.json).

up: Este comando crea e inicia los contenedores.

Verá los logs de todos los servicios en su terminal. El proceso puede tardar unos minutos la primera vez mientras se descargan las imágenes base y se instalan las dependencias.

Acceder a la Aplicación

Una vez que los contenedores se estén ejecutando, puede acceder a los diferentes servicios en su navegador web:

Aplicación del Juego (Frontend):
http://localhost:3000

Administrador de Base de Datos (Adminer):
http://localhost:8080

Para iniciar sesión en Adminer:

Sistema: SQLite

Base de datos: /app/instance/secuelas_game.db (Esta es la ruta al archivo de la base de datos dentro del contenedor del backend).

Detener la Aplicación
Para detener todos los servicios, presione Ctrl + C en la terminal donde ejecutó docker-compose up. Para eliminar los contenedores y las redes creadas, puede ejecutar:

docker-compose down

Desarrollo
Backend: Los cambios en los archivos .py del backend se recargarán automáticamente gracias al modo de depuración de Flask.

Frontend: Los cambios en los archivos .tsx o .css en la carpeta frontend/src se recargarán automáticamente en el navegador gracias al servidor de desarrollo de React. El volumen frontend/src:/app/src en docker-compose.yml asegura que los cambios en su máquina local se reflejen dentro del contenedor.