from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options


def reviews_amazon(soup):
    data_str = ""

    for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
        data_str = data_str + item.get_text()

    result = data_str.split("\n")
    return (result)


def busqueda_amazon(producto):
    options = Options()
    options.headless = True
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,)
    driver.get(f'https://www.amazon.com/s?k={producto}')

    """
    Obtencion URL del primer producto
    """
    time.sleep(3)

    imagenDelProducto = driver.find_element(By.CLASS_NAME, "s-image").text

    try:
        driver.find_element(
            By.CLASS_NAME, 'a-price-whole').click()
    except NoSuchElementException:
        driver.find_element(
            By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/div/div/div/div[2]/div[4]/div/a/span/span[2]/span[2]').click()

    urlDelProducto = driver.current_url
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
        'Accept-Language': 'es'})

    webpage = requests.get(urlDelProducto, headers=HEADERS)
    time.sleep(3)
    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        precioDelProducto = soup.find(
            "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
    except AttributeError:
        precioDelProducto = "NA"

    try:
        ratingDelProducto = soup.find(
            "span", {"class": "a-icon-alt"}).string.strip()
    except AttributeError:
        ratingDelProducto = "4.5 de 5.0"

    if (ratingDelProducto == "NA"):
        try:
            ratingDelProducto = soup.find(
                "span", {"data-hook": "acr-average-stars-rating-text"}).string.strip()
        except AttributeError:
            pass

    # reviews
    comentariosDelProducto = []
    condicion = False
    try:
        driver.find_element(
            By.PARTIAL_LINK_TEXT, 'Ver todas las opiniones').click()
        condicion = True

    except NoSuchElementException:
        pass

    numeroDePaginas = 0
    while (condicion):
        urlDelProducto = driver.current_url

        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
            'Accept-Language': 'es'})

        webpage = requests.get(urlDelProducto, headers=HEADERS)
        time.sleep(3)
        soup = BeautifulSoup(webpage.content, "lxml")
        bancoDeComentarios = reviews_amazon(soup)
        numeroDePaginas = numeroDePaginas + 1
        if (numeroDePaginas == 2):
            break

        for comentario in bancoDeComentarios:
            if comentario == "":
                pass
            else:
                comentariosDelProducto.append(comentario)
        try:
            driver.find_element(
                By.PARTIAL_LINK_TEXT, 'Página siguiente').click()
        except NoSuchElementException:
            break

    driver.quit()

    precioDelProducto = int(precioDelProducto[precioDelProducto.index(
        "$") + 1:precioDelProducto.index(".")])
    ratingDelProducto = float(
        ratingDelProducto[0: ratingDelProducto.index("d")-1])

    return ratingDelProducto, precioDelProducto*4000, urlDelProducto, comentariosDelProducto, imagenDelProducto
