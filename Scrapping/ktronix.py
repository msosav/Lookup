from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def busqueda_ktronix(nombre):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(
        executable_path="C:/SeleniumDrivers/chromedriver.exe")

    nombreFinal = nombre.replace(" ", "+")

    driver.get(f"https://www.ktronix.com/search/?text={nombreFinal}")
    driver.maximize_window()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "product__image__container").click()

    urlDeLaPagina = driver.current_url

    html_text = requests.get(urlDeLaPagina)
    time.sleep(3)

    soup = BeautifulSoup(html_text.text, 'lxml')
    nombreDelProducto = soup.find(
        "h1", class_="product-name__name").text

    imagen = soup.find('img', class_="image-modal-zoom-in")
    src = imagen.get('data-src')
    imagenDelProducto = (f"https://www.ktronix.com{src}")

    ratingDelProducto = driver.find_element(
        By.CLASS_NAME, "yotpo-star-digits").text
    ratingDelProducto = float(ratingDelProducto)

    precioDelProducto = soup.find(
        "span", class_="font-title--product-price").string.strip().replace('.', '')
    precioDelProducto = precioDelProducto.replace('$', '')
    precioDelProducto = int(precioDelProducto)

    tablaComentarios = driver.find_element(By.CLASS_NAME, "yotpo-reviews")
    bancoDeComentarios = tablaComentarios.find_elements(
        By.CLASS_NAME, "content-review")

    comentariosDelProducto = []

    for comentario in bancoDeComentarios:
        comentariosDelProducto.append(comentario.text)

    time.sleep(8)

    driver.quit()

    return (nombreDelProducto, imagenDelProducto, urlDeLaPagina, int(precioDelProducto),
            ratingDelProducto, comentariosDelProducto)
