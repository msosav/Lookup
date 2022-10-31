from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lenguaje_natural import procesamiento

from lenguaje_natural import procesamiento


def reviews_amazon(soup):
    data_str = ""

    for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
        data_str = data_str + item.get_text()

    result = data_str.split("\n")
    return (result)


def reviews_mercado(soup):
    data_str = ""

    for item in soup.find_all("p", class_="ui-review-capability-comments__comment__content"):
        data_str = data_str + item.get_text()
    result = soup
    result = data_str.split("\n")
    return (result)
# Busqueda en amazon


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
    try:
        driver.find_element(
            By.CLASS_NAME, 'a-price-whole').click()
    except NoSuchElementException:
        driver.find_element(
            By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/div/div/div/div[2]/div[4]/div/a/span/span[2]/span[2]').click()

    get_url = driver.current_url

    """
    Creacion header
    """

    URL = get_url
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
        'Accept-Language': 'es'})

    webpage = requests.get(URL, headers=HEADERS)
    time.sleep(3)
    soup = BeautifulSoup(webpage.content, "lxml")

    """
    Se busca el precio
    """
    try:
        product_price_raw = soup.find(
            "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
    except AttributeError:
        product_price_raw = "NA"

    """
    Se busca el rating
    """
    try:
        product_rating_raw = soup.find(
            "span", {"class": "a-icon-alt"}).string.strip()
    except AttributeError:
        product_rating_raw = "4.5 de 5.0"

    if (product_rating_raw == "NA"):
        try:
            product_rating_raw = soup.find(
                "span", {"data-hook": "acr-average-stars-rating-text"}).string.strip()
        except AttributeError:
            pass

    # reviews
    rev_result = []
    condicion = False
    try:
        driver.find_element(
            By.PARTIAL_LINK_TEXT, 'Ver todas las opiniones').click()
        condicion = True

    except NoSuchElementException:
        pass

    numPags = 0
    while (condicion):
        URL = driver.current_url

        URL = get_url
        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
            'Accept-Language': 'es'})

        webpage = requests.get(URL, headers=HEADERS)
        time.sleep(3)
        soup = BeautifulSoup(webpage.content, "lxml")
        rev_data = reviews_amazon(soup)
        numPags = numPags + 1
        if (numPags == 2):
            break

        for i in rev_data:
            if i == "":
                pass
            else:
                rev_result.append(i)
        try:
            driver.find_element(
                By.PARTIAL_LINK_TEXT, 'Página siguiente').click()
        except NoSuchElementException:
            break

    driver.quit()

    """
    Se limpian los strings resultantes
    """
    product_price = int(product_price_raw[product_price_raw.index(
        "$") + 1:product_price_raw.index(".")])
    product_rating = float(
        product_rating_raw[0: product_rating_raw.index("d")-1])

    return product_rating, product_price*4000, URL, rev_result


# Busqueda en mercadolibre
def busqueda_mercadolibre(producto):
    options = Options()
    options.headless = True
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(f'https://listado.mercadolibre.com.co/{producto}_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondición%26applied_filter_order%3D3%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D171%26is_custom%3Dfalse')

    time.sleep(3)
    """
    Obtencion URL del primer producto
    """
    driver.find_element(By.CLASS_NAME, "ui-search-item__title").click()

    get_url = driver.current_url

    """
    Creacion header
    """

    URL = get_url
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
        'Accept-Language': 'es'})

    webpage = requests.get(URL, headers=HEADERS)
    time.sleep(3)
    soup = BeautifulSoup(webpage.content, "lxml")

    """
    Se busca el precio
    """
    try:
        product_price_raw = soup.find(
            "span", attrs={'class': 'andes-money-amount__fraction'}).string.strip().replace('.', '')
    except AttributeError:
        product_price_raw = "NA"

    """
    Se busca el rating
    """
    #driver.find_element(By.CLASS_NAME, "ui-pdp-review__ratings").click()
    # time.sleep(3)
    product_rating_raw = driver.find_element(
        By.CLASS_NAME, 'ui-review-capability__rating').text

    driver.find_element(
        By.XPATH, '/html/body/div[2]/div[1]/div[2]/button[1]').click()

    driver.find_element(
        By.CLASS_NAME, 'show-more-click').click()

    time.sleep(3)

    driver.quit()

    """
    Se limpian los strings resultantes
    """
    product_price = int(product_price_raw.replace(".", ""))
    product_rating = float(product_rating_raw[0:3])

    rev_data = reviews_mercado(soup)
    rev_result = []
    for i in rev_data:
        if i == "":
            pass
        else:
            rev_result.append(i)

    return product_rating, product_price, URL, rev_result


def web_scrapping(producto):
    amazon = busqueda_amazon(producto)
    mercado = busqueda_mercadolibre(producto)

    arregloPortales = [amazon, mercado]

    rating = (arregloPortales[0][0] + arregloPortales[1][0])/2
    price = min(arregloPortales[0][1], arregloPortales[1][1])
    reviews = arregloPortales[0][3] + arregloPortales[1][3]
    reviewsSize = len(reviews)
    contBuenos = 0
    contMalos = 0

    topComments = ["", "", "", ""]

    for comentario in reviews:
        buenoOMalo = procesamiento(comentario)
        if (buenoOMalo):
            if contBuenos <= 1:
                topComments[contBuenos] = comentario
            contBuenos = contBuenos + 1
        else:
            if contMalos <= 1:
                topComments[contMalos+2] = comentario
            contMalos = contMalos + 1

    reviewRating = (5/reviewsSize)*contBuenos

    if rating > 4.5:
        comentariosRating = [topComments[0], topComments[1]]
    elif rating > 3.8:
        comentariosRating = [topComments[0], topComments[2]]
    else:
        comentariosRating = [topComments[2],  topComments[3]]

    if (arregloPortales[0][1] > arregloPortales[1][1]):
        URL = arregloPortales[1][2]
    else:
        URL = arregloPortales[0][2]

    return rating, price, URL, reviewRating, comentariosRating
