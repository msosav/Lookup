from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

<<<<<<< HEAD
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

digitos = [0,1,2,3,4,5,6,7,8,9]

#Mercado libre
def getMercadoLibre(item):
    driver.get('https://www.mercadolibre.com.co/')

    search_box = driver.find_element(by=By.NAME, value="as_word")
    search_box.send_keys(item)
    search_box.send_keys(Keys.RETURN)

    product = driver.find_element(By.CLASS_NAME, "ui-search-result-image__element")
    product.click()

    review = driver.find_element(By.CLASS_NAME, "ui-pdp-review__ratings")
    review.click()

    rating = driver.find_element(By.CLASS_NAME, "ui-review-view__rating__summary__average").text
    people = driver.find_element(By.CLASS_NAME, "ui-review-view__rating__summary__label").text
    #votes = people[people.index()]

    print(rating)
    print(people)

def getAliexpress(item):
    driver.get('https://es.aliexpress.com/?gatewayAdapt=glo2esp')

    search_box = driver.find_element(by=By.NAME, value="SearchText")
    search_box.send_keys(item)
    search_box.send_keys(Keys.RETURN)

    product = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/a[1]')
    product.click()

    driver.switch_to.window(driver.window_handles[-1])

    rating = float(driver.find_element(By.CLASS_NAME, 'overview-rating-average').text)
    people = driver.find_element(By.PARTIAL_LINK_TEXT("Valoraciones")).text


    print(rating)
    print(people)

def main():
    getMercadoLibre("iphone 11")

main()

driver.quit()
=======
def web_scrapping(item):
    #location = 'C:\\Users\\user\\Documents\\Proyectos semestre 4\\chromedriver.exe'
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    #Mercado libre
    driver.get('https://www.mercadolibre.com.co/')

    search_box = driver.find_element(by=By.NAME, value="as_word")
    search_box.send_keys(item)
    search_box.send_keys(Keys.RETURN)

    product = driver.find_element(By.CLASS_NAME, "ui-search-result-image__element")
    product.click()

    review = driver.find_element(By.CLASS_NAME, "ui-pdp-review__ratings")
    review.click()

    rating = driver.find_element(By.CLASS_NAME, "ui-review-view__rating__summary__average").text
    people = driver.find_element(By.CLASS_NAME, "ui-review-view__rating__summary__label").text

    return (rating, people)

    driver.quit()
>>>>>>> 348099b8f6bfbcb953ddce78255c77109033849e
