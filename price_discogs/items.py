# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceDiscogsItem(scrapy.Item):
    year = scrapy.Field()
    price = scrapy.Field()
    artist = scrapy.Field()
