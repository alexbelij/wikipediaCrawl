import scrapy
from hollywood.items import HollywoodItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class HollywoodActorsSpider(scrapy.Spider):
    name = "hollywoodActors"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Category:American_male_film_actors"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="mw-category-group"]/ul/li'):
            url = sel.xpath('a/@href').extract()[0]
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_contents)
        checkNextPage = response.xpath('//div[@id="mw-pages"]/a[contains(text(), "next page")]/attribute::*').extract()
        if(len(checkNextPage)>0):
            nextPageUrl = response.urljoin(checkNextPage[0])
            yield scrapy.Request(nextPageUrl, self.parse)


    def parse_contents(self, response):
        table = response.xpath('//table[@class="infobox biography vcard"]')
        item = HollywoodItem()
        spouses = table.xpath('//tr/th/span[contains(text(),"Spouse")]/ancestor::tr/td//text()').extract()
        item['actorFullName'] = table.xpath('//tr/th/span/text()')[0].extract()
        item['actorSpouses'] = spouses
        yield item






