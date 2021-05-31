import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//div[@data-qa-product]/a")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)
            '''
            Некоторые товары не открываются из-за редиректа:
            [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to <GET https://leroymerlin.ru/product/galeta-na-taburet-limony-35h35-sm-82709348/> from <GET https://leroymerlin.ru/product/galeta-na-taburet-limony-35x35-sm-82709348/>

            Хотела решить это при помощи регулярок, но не поняла куда засунуть условие, т.к. не во всех ссылках надо делать замену.
            if response.status == 301:
                clear_link = re.sub(r'(\d)h(\d)', r'\1x\2', response.url)
                yield response.follow(clear_link, callback=self.parse_good)
            '''

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('params', "//dt/text() | //dd/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        yield loader.load_item()
