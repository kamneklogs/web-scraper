from scrapy.http import Request
from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from bs4 import BeautifulSoup as bs


class Car(Item):
    """ A class that represents the items to be scraped (Cars) and its attributes"""
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


class MercadoLibreCrawler(Spider):
    """ A web-scraper for MercadoLibre website in the used cars section"""

    name = 'mercadolibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # 'CLOSESPIDER_PAGECOUNT': 2,  # Max number of pages to scrape items from.
    }

    allowed_domains = ['carros.mercadolibre.com.co', 'carro.mercadolibre.com.co']

    start_urls = ['https://carros.mercadolibre.com.co/usados/']

    def parse_start_url(self, response):
        """ Indicates the scraper to scrape the start url too

        :param response: the response to the request of the start url
        :return: None
        """
        return self.parse(response)

    def parse(self, response):
        """ Parses the response of the requested url in search of the cars details urls by their xpath
        and also extracts the next page page url by the xpath

        :param response: the response to a search page url request
        :return: None
        """
        cars = response.xpath('//div[@class="ui-search-result__image"]/a/@href').extract()
        # print(len(cars))
        for car in cars:
            yield Request(car, callback=self.parse_item)

        next_page_url = response.xpath(
            "//li[@class='andes-pagination__button andes-pagination__button--next']//a/@href").extract_first()
        #print(next_page_url)

        yield Request(next_page_url)

    def parse_item(self, response):
        """ Parses the response of a car detail url request in search of the attibutes of a car (that were
        defined in the class Car at the start of the file) by its unique xpath

        :param response: the response to a car detail url request
        :return: None
        """
        item = ItemLoader(Car(), response)

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
            if field == "kilometers":
                kms = response.xpath('//tr[' + str(idx + 1) + ']//td//span/text()').extract_first()
                item.add_value(field, kms.split(" ")[0])
            else:
                x_path = '//tr[' + str(idx + 1) + ']//td//span/text()'
                item.add_xpath(field, x_path)

        price = response.xpath('//span[@class="price-tag-fraction"]/text()').extract_first()
        item.add_value('price', price.replace(".", ""))

        yield item.load_item()