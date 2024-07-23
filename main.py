import requests
from bs4 import BeautifulSoup

# Definimos una función para limpiar el texto
def clean_text(text):
    """Eliminar espacios en blanco innecesarios y normalizar el texto."""
    return text.strip()

# Función principal para hacer scraping de las citas
def scrape_quotes():
    base_url = 'https://quotes.toscrape.com/page/' # URL base de la página.
    page = 1 # Empezamos en primera página.

    # Bucle while que recorre todas las paginas de la web.
    while True:
        url = f'{base_url}{page}/' # Construye URL de pagina actual.
        response = requests.get(url) # Obtiene contenido de la pagina.

        # Si la respuesta no es 200 (pagina no encontrada), se rompe el bucle.
        if response.status_code != 200:
            break

       # Analiza contenido HTML de la pagina web.     
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrae informacion de las citas.
        quote_containers = soup.find_all('div', class_='quote')
        # Si no hay citas se rompe el bucle.
        if not quote_containers:
            break
        
        # Bucle que extrae, muestra y limpia las frases, autores y tags.
        for container in quote_containers:
            quote = clean_text(container.find('span', class_='text').get_text())
            author = clean_text(container.find('small', class_='author').get_text())
            tags = [clean_text(tag.get_text()) for tag in container.find_all('a', class_='tag')]

            # Imprime información extraida (cita, autor y tags).
            print(f'Quote: {quote}')
            print(f'Author: {author}')
            print(f'Tags: {", ".join(tags)}')
            print('-' * 80) # Separación de cada cita para mejor visualización.

        # Pasa a la siguiente pagina.
        page += 1

# Ejecutamos la función principal solo si el script se ejecuta directamente
if __name__ == '__main__':
    scrape_quotes()

