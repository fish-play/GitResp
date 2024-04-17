# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydemoItem(scrapy.Item):
    # 要写对应电影的具体数据名称
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pingfen = scrapy.Field()

    pass
