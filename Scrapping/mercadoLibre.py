from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


def reviews_mercado(driver):
    comentariosDelProducto = []

    bancoDeComentarios = driver.find_element(
        By.CLASS_NAME, "ui-review-capability-filter")

    bancoDeComentarios = bancoDeComentarios.find_elements(
        By.CLASS_NAME, "ui-review-capability-comments__comment__content")

    time.sleep(4)

    for comentario in bancoDeComentarios:
        comentariosDelProducto.append(comentario.text)
    return comentariosDelProducto


# Busqueda en mercadolibre
def busqueda_mercadolibre(producto):
    options = Options()
    options.headless = True
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(f'https://listado.mercadolibre.com.co/{producto}_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondición%26applied_filter_order%3D3%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D171%26is_custom%3Dfalse')

    time.sleep(3)

    imagenDelProducto = driver.find_element(
        By.CLASS_NAME, "ui-search-result-image__element")

    imagenDelProducto = imagenDelProducto.get_attribute("src")

    driver.find_element(By.CLASS_NAME, "ui-search-item__title").click()

    urlDelProducto = driver.current_url
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
        'Accept-Language': 'es'})

    webpage = requests.get(urlDelProducto, headers=HEADERS)
    time.sleep(3)
    soup = BeautifulSoup(webpage.content, "lxml")

    nombreDelProducto = soup.find("h1", "ui-pdp-title")

    try:
        precioDelProducto = soup.find(
            "span", attrs={'class': 'andes-money-amount__fraction'}).string.strip().replace('.', '')
    except AttributeError:
        precioDelProducto = "NA"

    ratingDelProducto = driver.find_element(
        By.CLASS_NAME, 'ui-review-capability__rating').text

    time.sleep(8)

    ratingDelProducto = float(ratingDelProducto[0:3])

    comentariosDelProducto = reviews_mercado(driver)

    driver.quit()

    return (nombreDelProducto.text, imagenDelProducto, urlDelProducto,
            int(precioDelProducto), ratingDelProducto, comentariosDelProducto)
