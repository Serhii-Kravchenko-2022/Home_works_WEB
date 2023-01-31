import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


# creating class models for saving data uses scrapy item and field
class QuoteItem(Item):
    author = Field()
    quote = Field()
    tags = Field()


class AutorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    bio = Field()


# create class for get data from models and save to file
class SpiderPipeline(object):
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'author' in adapter.keys():
            self.quotes.append({
                'author': adapter['author'],
                'quote': adapter['quote'],
                'tags': adapter['tags']
            })

        if 'fullname' in adapter.keys():
            self.authors.append({
                'fullname': adapter['fullname'],
                'born_date': adapter['born_date'],
                'born_location': adapter['born_location'],
                'bio': adapter['bio']
            })
        return item

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False)

        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False)


# create main scrapy Spyder class
class Spider(scrapy.Spider):
    name = "my_spyder"

    allowed_domains = ['quotes.toscrape.com']  # input only domain name without http
    start_urls = ['http://quotes.toscrape.com']

# connect class for work with data
    custom_settings = {
        'ITEM_PIPELINES': {
            SpiderPipeline: 300
        }
    }

    def parse(self, response):
        """
        function for scraping data from HTML
        loop for get data from /html//div[@class="quote"]

        param response: response
        :return:
        """
        for q in response.xpath('/html//div[@class="quote"]'):
            quote = q.xpath('span[@class="text"]/text()').get().strip()
            author = q.xpath('span/small[@class="author"]/text()').get().strip()
            tags = q.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract()
            yield QuoteItem(quote=quote, author=author, tags=tags)
            yield response.follow(url=self.start_urls[0] + q.xpath('span/a/@href').get(), callback=self.parse_author)

        # for еру move through the pages, the button Next
        next_link = response.xpath('/html//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        """
        function for scraping data from HTML
        loop for get data from /html//div[@class="author-details"]

        :param response:
        :return:
        """
        body = response.xpath('/html//div[@class="author-details"]')
        fullname = body.xpath('h3[@class="author-title"]/text()').get().strip()
        born_date = body.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = body.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        bio = body.xpath('div[@class="author-description"]/text()').get().strip()
        yield AutorItem(fullname=fullname, born_date=born_date, born_location=born_location, bio=bio)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()
