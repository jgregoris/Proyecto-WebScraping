from scraper import scrape_quotes
from database import Database
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos usando variables de entorno
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def main():
    # Obtener las citas utilizando la función de scraping
    quotes = scrape_quotes()

    # Crear una instancia de la clase Database para conectar con la base de datos
    db = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

    try:
        # Insertar datos en la base de datos
        for quote in quotes:
            # Insertar o actualizar el autor y obtener su ID
            author_id = db.insert_author(quote['author'], {
                'bio': quote['author_bio'],
                'born_date': quote['author_born_date'],
                'born_location': quote['author_born_location']
            })
            # Insertar la cita y obtener su ID
            quote_id = db.insert_quote(quote['text'], author_id)
            # Insertar las etiquetas y asociarlas con la cita
            for tag in quote['tags']:
                tag_id = db.insert_tag(tag)
                db.insert_quote_tag(quote_id, tag_id)
        
        # Confirmar los cambios en la base de datos
        db.commit()
        print("Datos insertados correctamente en la base de datos.")
    except Exception as e:
        # En caso de error, revertir los cambios
        db.rollback()
        print(f"Error al insertar datos: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        db.close()

if __name__ == "__main__":
    # Ejecutar la función principal si este script se ejecuta directamente
    main()