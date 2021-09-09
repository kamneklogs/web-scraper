import requests
from bs4 import BeautifulSoup as bs

products = []  # Lista para guardar nombres de los autos
prices = []  # Lista para guardar precios

url = "https://loscoches.com/carros-usados/"

response = requests.get(url)
html = bs(response.text, 'html.parser')

vehicles_html = html.find_all('div', 'a.text', class_='car-content')

for vehicle in vehicles_html:
    item = vehicle.text.split('$')
    products.append(item[0])
    prices.append('$'+item[1])

for i in range(len(products)):
    print(products[i].strip() + ";" + prices[i])
