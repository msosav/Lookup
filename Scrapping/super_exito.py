from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def busqueda_exito(nombre):
    options = Options()
    options.headless = True
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,)

    nombreBarraNavegador = nombre.replace(" ", "%20")
    driver.get(
        f"https://www.exito.com/{nombreBarraNavegador}?_q={nombreBarraNavegador}&map=ft")
    time.sleep(4)

    producto = driver.find_element(
        By.CLASS_NAME, "vtex-product-summary-2-x-imageNormal")

    imagenDelProducto = producto.get_attribute('src')

    time.sleep(2)

    producto.click()

    urlDeLaPagina = driver.current_url

    time.sleep(3)

    nombreDelProducto = driver.find_element(
        By.CLASS_NAME, "vtex-store-components-3-x-productBrand")

    precioDelProducto = driver.find_element(
        By.CLASS_NAME, "exito-vtex-components-4-x-currencyContainer").text

    precioDelProducto = precioDelProducto.strip().replace('.', '')
    precioDelProducto = precioDelProducto.replace("$", "")
    precioDelProducto = precioDelProducto.replace(" ", "")
    precioDelProducto = int(precioDelProducto)

    try:
        ratingDelProducto = driver.find_element(
            By.CLASS_NAME, "exito-rating-by-sellers-0-x-ratingListQualityNumber")
    except:
        ratingDelProducto = None

    if ratingDelProducto != None:
        containerComentarios = driver.find_element(
            By.CLASS_NAME, "exito-rating-by-sellers-0-x-ratingListQualityContainer")
        comentariosDelProductoAux = containerComentarios.find_elements(
            By.CLASS_NAME, "exito-rating-by-sellers-0-x-ratingListQualityItemMessage")
        time.sleep(5)

        comentariosDelProducto = []
        for comentario in comentariosDelProductoAux:
            comentariosDelProducto.append(comentario.text)

        return (nombreDelProducto.text, imagenDelProducto, urlDeLaPagina, int(precioDelProducto),
                float(ratingDelProducto.text), comentariosDelProducto)
    time.sleep(5)
    return (nombreDelProducto.text, imagenDelProducto, urlDeLaPagina, int(precioDelProducto))
