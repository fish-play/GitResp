"""
-*- coding: utf-8 -*-
@Time : 2024/2/18 10:59
"""
import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from scrapydemo.items import ScrapydemoItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allower_domains = ["mover.douban.com"]

    # 起始页面的网址
    def start_requests(self):
        for page in range(10):
            yield Request(url=f"https://movie.douban.com/top250?start={page * 25}&filter=")
            # 加代理的话用 国外用socks,国内就https
            yield Request(url=f"https://movie.douban.com/top250?start={page * 25}&filter=",
                          meta={"proxy": 'socks5://127.0.0.1:10808'})

    def parse(self, response: HtmlResponse, **kwargs):
        """目前没找到原因，用css可以正常拿到数据，xpath会重复拿"""
        sel = Selector(response)
        # list_items = sel.xpath('//*[@id="content"]//ol/li')
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = ScrapydemoItem()
            # movie_item["title"] = list_item.xpath('//span[@class="title"]/text()').extract()
            movie_item["title"] = list_item.css('span.title::text').extract_first()
            # movie_item["pingfen"] = list_item.xpath('//span[@class="rating_num"]/text()').extract()
            movie_item["pingfen"] = float(list_item.css('span.rating_num::text').extract_first())
            yield movie_item

