import requests
from bs4 import BeautifulSoup
import time

# URL base del sitio web de citas
BASE_URL = "https://quotes.toscrape.com"

def get_page_content(url):
    """
    Obtiene el contenido HTML de una URL.
    """
    try:
        # Realiza una solicitud GET a la URL
        response = requests.get(url)
        # Genera una excepción si ocurre un error HTTP
        response.raise_for_status()
        # Retorna el contenido de la respuesta
        return response.content
    except requests.exceptions.RequestException as e:
        # Imprime un mensaje de error y retorna None
        print(f"Error al obtener la página {url}: {e}")
        return None

def clean_text(text):
    # Elimina los espacios en blanco al principio y al final del texto
    return text.strip()

def scrape_quotes():
    """
    Extrae citas de todas las páginas del sitio web y obtiene información de los autores.
    """
    quotes = []  # Lista para almacenar todas las citas
    url = BASE_URL + "/page/1/"  # URL de la primera página de citas
    
    while url:
        # Obtiene el contenido HTML de la página actual
        html = get_page_content(url)
        if html is None:
            break  # Si no se pudo obtener el contenido, salir del bucle
        # Crea un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')
        # Encuentra todos los elementos de citas en la página
        quote_elements = soup.find_all('div', class_='quote')
        
        for quote_element in quote_elements:
            # Extrae y limpia el texto de la cita
            text = clean_text(quote_element.find('span', class_='text').get_text())
            # Extrae y limpia el nombre del autor
            author = clean_text(quote_element.find('small', class_='author').get_text())
            # Extrae y limpia las etiquetas asociadas a la cita
            tags = [clean_text(tag.get_text()) for tag in quote_element.find_all('a', class_='tag')]
            # Construye la URL de la página del autor
            author_url = BASE_URL + quote_element.find('a')['href']
            
            # Extrae la información del autor
            author_info = scrape_author_info(author_url)
            
            # Añade la cita y la información del autor a la lista de citas
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags,
                'author_bio': author_info.get('bio'),
                'author_born_date': author_info.get('born_date'),
                'author_born_location': author_info.get('born_location')
            })
        
        # Encuentra el enlace a la siguiente página
        next_page = soup.find('li', class_='next')
        # Actualiza la URL para la próxima iteración si hay una siguiente página
        url = BASE_URL + next_page.find('a')['href'] if next_page else None
        # Espera un segundo antes de la siguiente solicitud para evitar sobrecargar el servidor
        time.sleep(1)
    
    return quotes  # Retorna la lista completa de citas y su información

def scrape_author_info(url):
    """
    Extrae información del autor desde su página de "about".
    """
    # Obtiene el contenido HTML de la página del autor
    html = get_page_content(url)
    if html is None:
        return {'bio': 'No disponible', 'born_date': 'No disponible', 'born_location': 'No disponible'}
    # Crea un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Diccionario para almacenar la información del autor
    author_info = {}
    # Extrae y limpia la biografía del autor
    author_info['bio'] = clean_text(soup.find('div', class_='author-description').get_text())
    # Extrae y limpia la fecha de nacimiento del autor
    born_info = clean_text(soup.find('span', class_='author-born-date').get_text())
    # Extrae y limpia el lugar de nacimiento del autor
    born_location = clean_text(soup.find('span', class_='author-born-location').get_text())
    # Almacena la fecha y lugar de nacimiento en el diccionario
    author_info['born_date'] = born_info
    author_info['born_location'] = born_location
    
    return author_info  # Retorna el diccionario con la información del autor

if __name__ == '__main__':
    # Extrae todas las citas y su información
    quotes = scrape_quotes()
    # Imprime cada cita y la información asociada
    for quote in quotes:
        print(f"Quote: {quote['text']}")
        print(f"Author: {quote['author']}")
        print(f"Tags: {', '.join(quote['tags'])}")
        print(f"Author Bio: {quote['author_bio']}")
        print(f"Author Born Date: {quote['author_born_date']}")
        print(f"Author Born Location: {quote['author_born_location']}")
        print("-" * 80)


