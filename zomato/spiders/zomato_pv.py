import scrapy


class ZomatoPvSpider(scrapy.Spider):
    name = "zomato_pv"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
