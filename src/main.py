import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

products = []  # Lista para guardar nombres de los autos
prices = []  # Lista para guardar precios

url = "https://loscoches.com/carros-usados/?cars_pp=48&cars_orderby=date&cars_order=asc&lay_style=view-grid-left&cars_grid=yes"

response = requests.get(url)
html = bs(response.text, 'html.parser')

vehicles_html = html.find_all('div', 'a.text', class_='car-content')

vehicles_html


# col-lg-4 col-md-4 col-sm-4 col-xs-6
# col-lg-4 col-md-4 col-sm-4 col-xs-6
# col-lg-4 col-md-4 col-sm-4 col-xs-6

entradas = html.find_all(
    'div', {'class': 'col-lg-4 col-md-4 col-sm-4 col-xs-6'})
entradas

len(entradas)


for i, entrada in enumerate(entradas):
    titulo = entrada.find(
        'div', class_='car-content').getText().split('$')[0].strip()

    precio = entrada.find(
        'div', class_='car-content').getText().split('$')[1].strip()

    anioYkilometraje = entrada.find(
        'ul', class_='list-inline').getText().strip().split(' ')
    anio = anioYkilometraje[0]
    kilometraje = anioYkilometraje[1]

    print('{};{};{};{}'.format( titulo, precio, anio, kilometraje))
