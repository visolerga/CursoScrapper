import requests
from bs4 import BeautifulSoup

# Función para obtener el contenido de la página web
def fetch_webpage(url):
    # Encabezados para simular una solicitud de un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Realizar la solicitud GET con los encabezados
        response = requests.get(url, headers=headers)
        # Levantar un error para códigos de estado HTTP 4xx/5xx
        response.raise_for_status()
        # Devolver el contenido de la página
        return response.text
    except requests.exceptions.RequestException as e:
        # Imprimir un mensaje de error si ocurre un problema con la solicitud
        print(f"Error al acceder a la página web: {e}")
        return None

# Función para guardar el contenido en un archivo
def save_to_file(content, filename):
    try:
        # Abrir el archivo en modo de escritura con codificación UTF-8
        with open(filename, 'w', encoding='utf-8') as file:
            # Escribir el contenido en el archivo
            file.write(content)
        print(f"El contenido de la página web se ha guardado en {filename}")
    except IOError as e:
        # Imprimir un mensaje de error si ocurre un problema al escribir el archivo
        print(f"Error al escribir en el archivo: {e}")

# Función principal para ejecutar el proceso de scraping
def main(url):
    # Obtener el contenido de la página web
    webpage_content = fetch_webpage(url)
    if webpage_content:
        # Guardar el contenido en un archivo si se obtuvo correctamente
        save_to_file(webpage_content, 'web.txt')

# Verificar si el script se está ejecutando directamente
if __name__ == "__main__":
    # URL de la página web objetivo
    url = 'https://www.chollometro.com/ofertas/cursos-gratis-de-photoshop-chatgpt-excel-java-php-python-after-effect-aws-wordpress-y-otros-udemy-1297415'
    # Ejecutar el proceso de scraping
    main(url)
