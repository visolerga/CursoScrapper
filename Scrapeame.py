import requests  # Importar el módulo 'requests' para realizar solicitudes HTTP
import re  # Importar el módulo 're' para utilizar expresiones regulares
import html

# Función para obtener el contenido de una página web dada una URL
def fetch_webpage(url):
    headers = {  # Definir encabezados HTTP para simular un navegador
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)  # Realizar una solicitud GET a la URL proporcionada
        response.raise_for_status()  # Generar una excepción si la solicitud no tiene éxito
        return response.text  # Devolver el contenido de la página web como texto
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página web: {e}")  # Imprimir un mensaje de error si ocurre una excepción
        return None  # Devolver 'None' si ocurre un error

def save_to_file(content, filename):
    try:
        # Desescapar caracteres Unicode
        content = html.unescape(content)
        content = content.encode('ascii', 'ignore').decode('utf-8')  # Eliminar caracteres Unicode

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"El contenido se ha guardado en {filename}")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

# Función para extraer títulos de elementos <li> de una página web y guardarlos en un archivo
def extract_li_titles(content, filename):
    try:
        # Expresión regular para encontrar todos los elementos <li> y </li>
        li_regex = re.compile(r'<li>(.*?)li>', re.DOTALL)
        # Encontrar todos los elementos <li> y </li> usando la expresión regular
        li_elements = li_regex.findall(content)
        # Guardar los elementos <li> en un archivo para revisarlos
        save_to_file('\n'.join(li_elements), filename)
        print(f"Los elementos <li> se han guardado en {filename}")

        # Expresión regular para verificar si los elementos <li> contienen el atributo title
        title_regex = re.compile(r'title=\\"([^"]*?)\\"')
        # Guardar los títulos en un archivo separados por nuevas líneas
        with open('Titulos.txt', 'w', encoding='utf-8') as file:
            for li_element in li_elements:
                # Desescapar caracteres especiales HTML
                li_element = html.unescape(li_element)

                # Buscar si el elemento <li> contiene el atributo title
                title_match = title_regex.search(li_element)
                if title_match:
                    title = title_match.group(1).strip()
                    file.write(title + '\n')
        print(f"Los títulos se han guardado en Titulos.txt")
    except Exception as e:
        print(f"Error al extraer los títulos: {e}")  # Imprimir un mensaje de error si ocurre una excepción

# Función principal que ejecuta el código
def main(url):
    webpage_content = fetch_webpage(url)  # Obtener el contenido de la página web
    if webpage_content:  # Si se obtiene el contenido de la página web correctamente
        extract_li_titles(webpage_content, 'Tabla.txt')  # Extraer títulos de elementos <li> y guardarlos en un archivo

if __name__ == "__main__":
    #url = 'https://www.chollometro.com/ofertas/cursos-gratis-de-photoshop-chatgpt-excel-java-php-python-after-effect-aws-wordpress-y-otros-udemy-1297415'
    #url = 'https://www.chollometro.com/ofertas/cursos-online-gratuitos-por-tiempo-limitado-udemy-1296729'
    url = 'https://www.chollometro.com/ofertas/cursos-en-espanol-gratuitos-por-tiempo-limitado-udemy-1299966'
    main(url)  # Llamar a la función principal con la URL proporcionada como argumento
