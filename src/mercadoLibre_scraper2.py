from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup as bs


class Car(Item):
    brand = Field()
    model = Field()
    year = Field()
    color = Field()
    fuel_type = Field()
    doors = Field()
    transmission = Field()
    motor = Field()
    bodywork_type = Field()
    kilometers = Field()
    price = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 1,
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    # Utilizamos 2 dominios permitidos, ya que los articulos utilizan un dominio diferente
    allowed_domains = ['carros.mercadolibre.com.co', 'carro.mercadolibre.com.co']

    start_urls = ['https://carros.mercadolibre.com.co/usados/']

    download_delay = 1

    # Tupla de reglas
    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+'
                # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/MCO-',
                restrict_xpaths='//div[@class="ui-search-result__image"]'
            ), follow=True, callback='parse_items'),
        # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):
        item = ItemLoader(Car(), response)

        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?

        dict_fields = {
            "Marca": "brand",
            "Modelo": "model",
            "Año": "year",
            "Color": "color",
            "Tipo de combustible": "fuel_type",
            "Puertas": "doors",
            "Transmisión": "transmission",
            "Motor": "motor",
            "Tipo de carrocería": "bodywork_type",
            "Kilómetros": "kilometers"
        }

        html = bs(response.text, 'html.parser')
        ths = list(map(lambda x: x.getText(), html.find_all('th')))  # name of <th> tags

        fields = []

        for th in ths:
            fields.append(dict_fields.get(th))

        for idx, field in enumerate(fields):
            x_path = '//tr[' + str(idx+1) + ']//td//span/text()'
            item.add_xpath(field, x_path)

        item.add_xpath('price', '//span[@class="price-tag-fraction"]/text()')

        yield item.load_item()
