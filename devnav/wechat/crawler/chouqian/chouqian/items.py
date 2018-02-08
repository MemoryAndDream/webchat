# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChouqianItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    page_url = scrapy.Field()
    desc = scrapy.Field()
    img_url = scrapy.Field()
    pass


class AlibabaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    category_id = scrapy.Field()
    QuickDetails = scrapy.Field()