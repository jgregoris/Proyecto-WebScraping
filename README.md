# Proyecto Web Scraping

Este proyecto realiza web scraping de citas, las almacena en una base de datos PostgreSQL y proporciona una interfaz de usuario con Streamlit para visualizar y explorar las citas.

## Requisitos previos

- Python 3.7+
- PostgreSQL
- pip (gestor de paquetes de Python)
- Streamlit
  
## Configuración

1. Clona este repositorio:
   
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

2. Crea un entorno virtual e instala las dependencias:

python -m venv venv

Para Windows:
venv\Scripts\activate

Para macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt

3. Configura la base de datos PostgreSQL:
- Crea una nueva base de datos en PostgreSQL
- Copia el archivo `.env.example` a `.env` y actualiza las variables con tus credenciales de PostgreSQL

## Ejecución del script de scraping

Para ejecutar el script de scraping y almacenar los datos en PostgreSQL:

python main.py

## Almacenamiento de datos en PostgreSQL

El script `main.py` se encarga de insertar los datos extraídos en la base de datos PostgreSQL. Asegúrate de que las credenciales en tu archivo `.env` sean correctas y que la base de datos esté creada antes de ejecutar el script.

## Visualización con Streamlit

Para ejecutar la aplicación Streamlit y visualizar los datos:

streamlit run app.py

Esto iniciará un servidor local y abrirá la aplicación en tu navegador predeterminado. Si no se abre automáticamente, puedes acceder a la aplicación en `http://localhost:8501`.

## Estructura del proyecto

- `main.py`: Script principal para el web scraping y almacenamiento de datos
- `scraper.py`: Contiene la lógica de web scraping
- `database.py`: Maneja las operaciones de la base de datos
- `app.py`: Aplicación Streamlit para visualizar los datos
- `.env`: Archivo de configuración para las variables de entorno (no incluido en el repositorio)

## Notas adicionales

- Asegúrate de respetar los términos de servicio del sitio web del que estás extrayendo datos.
- Este proyecto es solo para fines educativos y de demostración.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un pull request.
