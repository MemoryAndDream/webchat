# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: cou_qian_spider.py 
@time: 2018/1/10 13:45 
"""

import scrapy

from chouqian.items import ChouqianItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class ChouqianSpider(scrapy.Spider):
    print 'Chouqian start'
    name = "chouqian"  # 唯一标识
    # allowed_domains = ["csdn.net"]
    start_urls = [
        "http://www.sheup.com/constellationmatch/guanyinlingqian/guanyin8.htm",

    ]

    #def start_requests(self): #测试cookie
    #    # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
    #    yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies={'meng':1})

    def parse(self, response):
        #loader = ItemLoader(item=ChouqianItem(), response=response)  # ItemLoader好像能配置多个xpath，css选择器，然后第一个选出来的作为结果
        #loader.add_xpath('img_url', '//span[@class="span_right"]/a/img/@src')
        #print loader.get_value(u'name: foo', TakeFirst(), unicode.upper, re='name: (.+)')
        #loader.add_value('name', u'name: foo', TakeFirst(), re='name: (.+)')
        #yield loader.load_item()  # 将结果返回为item
        base_url = get_base_url(response)
        rs_item = ChouqianItem()
        rs_item['img_url'] ='http://www.sheup.com/constellationmatch'+ response.xpath('//span[@class="span_right"]/a/img/@src').extract_first()
        rs_item['title'] = response.xpath('//h1/text()').extract_first()
        rs_item['page_url'] = base_url
        yield rs_item
        next_page = response.xpath('//div[@class="rel1_text_2"]//li/a/@href').extract()
        for url in next_page:
            url = urljoin_rfc(base_url, url)
            yield scrapy.Request(url = url)#没有callback默认就还是这个

