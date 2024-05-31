import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
from datetime import datetime
import os

# Configuración de la conexión a la base de datos MySQL
db_config = {
    'user': 'scrapper',
    'password': 'scrapper',
    'host': '127.0.0.1',
    'database': 'scrapperdb',
    'port': '3306'
}

# Configurar la base de datos MySQL
def setup_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS web_content (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        link_text TEXT NOT NULL,
                        link_url TEXT NOT NULL,
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

# Función para obtener y analizar la página web usando Selenium
def fetch_webpage(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin abrir una ventana del navegador)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Obtener la ruta del ChromeDriver utilizando webdriver-manager
    chrome_driver_path = ChromeDriverManager().install()

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    driver.get(url)
    
    # Esperar explícitamente hasta que los elementos se carguen
    driver.implicitly_wait(10)
    
    # Imprimir el HTML de la página para verificar que se carga correctamente
    page_source = driver.page_source
    print(page_source)
    
    # Actualizar el selector CSS para buscar los elementos <a> dentro de <li>
    elements = driver.find_elements(By.CSS_SELECTOR, 'li a.link')
    links = [{'text': elem.text.strip(), 'url': elem.get_attribute('href')} for elem in elements]
    driver.quit()
    return links

# Función para actualizar la base de datos con nuevos contenidos y rastrear cambios
def update_database(new_contents):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Obtener los contenidos actuales
    cursor.execute('SELECT link_text, link_url FROM web_content')
    current_contents = {(row[0], row[1]) for row in cursor.fetchall()}

    # Insertar nuevos contenidos y rastrear cambios
    for content in new_contents:
        if (content['text'], content['url']) not in current_contents:
            cursor.execute('INSERT INTO web_content (link_text, link_url) VALUES (%s, %s)', (content['text'], content['url']))
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
url = 'https://www.chollometro.com/ofertas/cursos-gratis-de-photoshop-chatgpt-excel-java-php-python-after-effect-aws-wordpress-y-otros-udemy-1297415'  # Reemplaza con la URL de la página web objetivo
run_scraper(url)
