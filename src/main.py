from selenium import webdriver  # Para controlar chromium, automatizada
from bs4 import BeautifulSoup  # Scrapping mediante localización de componentes
import pandas as pd  # Pandas, just pandas jaj


# Directorio de chromium con chromedriver (Ext descargable, verificar compatibilidad de estensión y browser)
driver = webdriver.Chrome("/usr/lib64/chromium-browser/chromedriver")

products = []  # Lista para guardar nombres de los autos
prices = []  # Lista para guardar precios


# https://loscoches.com/carros-usados/ Pagina objetivo
# car-content   class de nombre de autos en el html
# new-price    class de precios "                   "

driver.get("https://loscoches.com/carros-usados/")  # Manipulación de chromium
content = driver.page_source  # Referencia a fuente de la pagina
soup = BeautifulSoup(content)
