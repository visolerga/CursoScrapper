import requests
import re

def fetch_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página web: {e}")
        return None

def save_to_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"El contenido se ha guardado en {filename}")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

def extract_li_titles(content, filename):
    try:
        # Expresión regular para encontrar todos los elementos <li> y </li>
        li_regex = re.compile(r'<li>(.*?)li>', re.DOTALL)
        # Encontramos todos los elementos <li> y </li> usando la expresión regular
        li_elements = li_regex.findall(content)
        # Guardamos los elementos <li> en un archivo para revisarlos
        save_to_file('\n'.join(li_elements), filename)
        print(f"Los elementos <li> se han guardado en {filename}")

        # Expresión regular para verificar si los elementos <li> contienen el atributo title
        title_regex = re.compile(r'title=\"([^"]*?)\"')
        # Guardamos los títulos en un archivo separados por nuevas líneas
        with open('Titulos.txt', 'w', encoding='utf-8') as file:
            for li_element in li_elements:
                # Buscamos si el elemento <li> contiene el atributo title
                title_match = title_regex.search(li_element)
                if title_match:
                    title = title_match.group(1).strip()
                    file.write(title + '\n')
        print(f"Los títulos se han guardado en Titulos.txt")
    except Exception as e:
        print(f"Error al extraer los títulos: {e}")

def main(url):
    webpage_content = fetch_webpage(url)
    if webpage_content:
        extract_li_titles(webpage_content, 'Tabla.txt')

if __name__ == "__main__":
    url = 'https://www.chollometro.com/ofertas/cursos-gratis-de-photoshop-chatgpt-excel-java-php-python-after-effect-aws-wordpress-y-otros-udemy-1297415'
    main(url)
