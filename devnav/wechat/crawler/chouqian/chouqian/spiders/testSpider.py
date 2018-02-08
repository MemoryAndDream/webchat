# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: testSpider.py 
@time: 2018/1/12 14:06 
"""

import scrapy

from chouqian.items import ChouqianItem


class testSpider(scrapy.Spider):
    print 'csdn start'
    name = "test"  # 唯一标识
    #allowed_domains = ["csdn.net"]
    start_urls = [
        "http://www.sheup.com/constellationmatch/guanyinlingqian/guanyin8.htm",
    ]

    def parse(self, response):
        for sel in response.xpath('//dl[@class="search-list"]'):
            item = ChouqianItem()

            item['img_url'] = sel.xpath('//p[@align="center"]/img').extract()

            url = response.url
            yield item  # 将结果返回为item