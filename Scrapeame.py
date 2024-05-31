import requests

def fetch_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # Aquí retornamos el contenido HTML
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página web: {e}")
        return None

def save_to_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"El contenido de la página web se ha guardado en {filename}")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

def main(url):
    webpage_content = fetch_webpage(url)
    if webpage_content:
        save_to_file(webpage_content, 'web.html')  # Cambiamos el nombre del archivo a 'web.html'

if __name__ == "__main__":
    url = 'https://www.chollometro.com/ofertas/cursos-gratis-de-photoshop-chatgpt-excel-java-php-python-after-effect-aws-wordpress-y-otros-udemy-1297415'
    main(url)
