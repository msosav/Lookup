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

#Busqueda en amazon
def busqueda_amazon(producto):
    options = Options()
    options.headless = True 
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options )
    driver.get(f'https://www.amazon.com/s?k={producto}')
    
    
    """
    Obtencion URL del primer producto
    """
    try:
        driver.find_element(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']").click()
    except NoSuchElementException:
        driver.find_element(By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']").click()


    get_url = driver.current_url
    driver.quit()

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
            "span", {"class":"a-icon-alt"}).string.strip()
    except AttributeError:
        product_rating_raw= "NA"

    """
    Se limpian los strings resultantes
    """
    product_price = float(product_price_raw[product_price_raw.index("$") + 1:])
    product_rating = float(product_rating_raw[0: product_rating_raw.index("d")-1])

    return product_rating, product_price, URL



#Busqueda en mercadolibre
def busqueda_mercadolibre(producto):
    options = Options()
    options.headless = True 
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)
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
    product_rating_raw = driver.find_element(By.CLASS_NAME, "ui-review-view__rating__summary__average").text
    driver.quit()

    """
    Se limpian los strings resultantes
    """
    product_price = float(product_price_raw.replace(".", ""))
    product_rating = float(product_rating_raw)

    return product_rating, product_price, URL

def webScrapping(producto):
    amazon = busqueda_amazon(producto)
    mercado = busqueda_mercadolibre(producto)

    arregloPortales = [amazon, mercado]

    rating = (arregloPortales[0][0] + arregloPortales[1][0])/2
    price = max((arregloPortales[0][1]*4), arregloPortales[1][1] )
    if(arregloPortales[0][1] > arregloPortales[1][1]):
        URL = arregloPortales[1][2]
    else:
        URL = arregloPortales[0][2]

    return rating, price, URL

