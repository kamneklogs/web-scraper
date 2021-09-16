from scrapy.http import Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
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

class BooksScrapySpider(Spider):
    name = 'mercadolibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 2,  # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    allowed_domains = ['carros.mercadolibre.com.co', 'carro.mercadolibre.com.co']

    start_urls = ['https://carros.mercadolibre.com.co/usados/']

    def parse_start_url(self, response):
        return self.parse(response)

    def parse(self, response):
        cars = response.xpath('//div[@class="ui-search-result__image"]/a/@href').extract()
        # print(len(cars))
        for car in cars:
            yield Request(car, callback=self.parse_item)

        next_page_url = response.xpath(
            "//li[@class='andes-pagination__button andes-pagination__button--next']//a/@href").extract_first()
        print(next_page_url)

        yield Request(next_page_url)

    def parse_item(self, response):
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
            x_path = '//tr[' + str(idx + 1) + ']//td//span/text()'
            item.add_xpath(field, x_path)

        item.add_xpath('price', '//span[@class="price-tag-fraction"]/text()')

        yield item.load_item()