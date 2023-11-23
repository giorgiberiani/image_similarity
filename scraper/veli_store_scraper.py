import scrapy
from scrapy.crawler import CrawlerProcess


categories = [
    "/category/sachuqrebis-veli/4666/",
    "/category/fasdaklebebi/5398/",
    "/category/tsveuleba/3106/",
    "/category/saakhaltslo-mzadeba/2350/",
    "/category/silamaze-movla/175/",
    "/category/teqnika/774/",
    "/category/sakhli-ezo/1178/",
    "/category/sakhlis-movla/308/",
    "/category/mshobeli-bavshvi/188/",
    "/category/soflidan/5687/",
    "/category/sachuqrebi/2264/",
    "/category/bari-meti/1561/",
    "/category/avto-moto/2329/",
    "/category/ckhovelebis-movla/1376/",
    "/category/sporti-mogzauroba/4981/",
    "/category/tsignebi/62/",
    "/category/fitnesi-ioga/1775/",
    "/category/sakancelario-krafti/114/",
    "/category/pylones/4641/",
    "/category/kikkerland/1866/",
    "/category/yoveldghiuri-sayidlebi/5196/"
]


class VeliStoreSpider(scrapy.Spider):
    name = "veli"
    base_url = "https://veli.store"

    start_urls = [url.replace("/category/", "https://veli.store/category/") for url in categories]


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_category)
    def parse_category(self, response):
        _categories = response.xpath('//*[@id="__next"]/section/div/div/ul/a/@href').extract()
        for category in _categories:
            for i in range(25):
                url = f'{self.base_url}{category}?page={i}'
                yield scrapy.Request(url=url, callback=self.parse_sub_category)

    def parse_sub_category(self, response):
        items_urls = response.xpath('//*[@id="__next"]/section/div/div[4]/div[4]/div/a/@href').extract()
        for item_url in items_urls:
            yield scrapy.Request(url=f'{self.base_url}{item_url}', callback=self.parse_item)

    def parse_item(self, response):
        item = {}
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['price'] = response.xpath('//h3[@class="price"]//text()').extract()
        item['image'] = response.xpath('//img/@src').extract_first()
        yield item



if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(VeliStoreSpider)
    process.start() 

