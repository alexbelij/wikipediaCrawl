import scrapy
from hollywood.items import HollywoodItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class HollywoodActorsSpider(scrapy.Spider):
    name = "hollywoodActresses"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_American_film_actresses"
    ]

    def parse(self, response):
        divs = response.xpath('//div[@id="mw-content-text"]')
        for sel in response.xpath('//div[@id="mw-content-text"]/div[@class="div-col columns column-width"]/ul/li'):
            url = sel.xpath('a/@href').extract()[0]
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_contents)


    def parse_contents(self, response):
        table = response.xpath('//table[@class="infobox biography vcard"]')
        item = HollywoodItem()
        spouses = table.xpath('//tr/th/span[contains(text(),"Spouse")]/ancestor::tr/td//text()').extract()
        item['actorFullName'] = table.xpath('//tr/th/span/text()')[0].extract()
        item['actorSpouses'] = spouses
        yield item






