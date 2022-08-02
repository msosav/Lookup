from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.mercadolibre.com.co/apple-iphone-11-128-gb-negro/p/MCO15149567?pdp_filters=category:MCO1055#reviews-summary'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Rating
rating = (soup.find('p', class_="ui-review-view__rating__summary__average")).text

#People
pple = (soup.find('span', class_="ui-pdp-review__amount")).text
people = pple[pple.index("(")+1 : pple.index(")")]



print(people)
