import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

products = []  
prices = []  
years = []  
kilometers = [] 


url = "https://loscoches.com/carros-usados/?cars_pp=48&cars_orderby=date&cars_order=asc&lay_style=view-grid-left&cars_grid=yes"

response = requests.get(url)
html = bs(response.text, 'html.parser')

vehicles_html = html.find_all('div', 'a.text', class_='car-content')

inputs = html.find_all(
    'div', {'class': 'col-lg-4 col-md-4 col-sm-4 col-xs-6'})


for i, entrada in enumerate(inputs):

    products.append(entrada.find(
        'div', class_='car-content').getText().split('$')[0].strip())

    prices.append(entrada.find(
        'div', class_='car-content').getText().split('$')[1].strip())

    anioYkilometraje = entrada.find(
        'ul', class_='list-inline').getText().strip().split(' ')

    years.append(anioYkilometraje[0])

    kilometers.append(anioYkilometraje[1])


df = pd.DataFrame({'Model': products, 'Price': prices,
                  'year': years, 'kms': kilometers})

df.to_csv('cars.csv', index=False, encoding='utf-8')
