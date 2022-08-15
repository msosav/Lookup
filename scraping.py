from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#location = 'C:\\Users\\user\\Documents\\Proyectos semestre 4\\chromedriver.exe'
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#Producto
item = "iphone 11"

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

print(rating)
print(people)

driver.quit()
