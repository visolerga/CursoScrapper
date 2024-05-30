import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

# Configuración de la conexión a la base de datos MySQL
db_config = {
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'host': 'your_mysql_host',  # e.g., 'localhost' or '127.0.0.1'
    'database': 'your_database_name',
    'port': 'your_mysql_port'   # e.g., 3306
}

# Configurar la base de datos MySQL
def setup_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS web_content (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                     )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS content_changes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        content_id INT,
                        change_type VARCHAR(50) NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(content_id) REFERENCES web_content(id)
                     )''')
    conn.commit()
    cursor.close()
    conn.close()

# Función para obtener y analizar la página web
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return [item.text.strip() for item in soup.find_all('p')]  # Ejemplo: scraping de todos los <p> tags
    else:
        return []

# Función para actualizar la base de datos con nuevos contenidos y rastrear cambios
def update_database(new_contents):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Obtener los contenidos actuales
    cursor.execute('SELECT content FROM web_content')
    current_contents = {row[0] for row in cursor.fetchall()}

    # Insertar nuevos contenidos y rastrear cambios
    for content in new_contents:
        if content not in current_contents:
            cursor.execute('INSERT INTO web_content (content) VALUES (%s)', (content,))
            content_id = cursor.lastrowid
            cursor.execute('INSERT INTO content_changes (content_id, change_type) VALUES (%s, %s)', (content_id, 'added'))

    conn.commit()
    cursor.close()
    conn.close()

# Función principal para ejecutar el scraper
def run_scraper(url):
    new_contents = fetch_webpage(url)
    if new_contents:
        update_database(new_contents)
    else:
        print('No se pudo obtener la página web o no se encontró contenido.')

# Configurar la base de datos y ejecutar el scraper
setup_database()
url = 'http://example.com'  # Reemplaza con la URL de la página web objetivo
run_scraper(url)
