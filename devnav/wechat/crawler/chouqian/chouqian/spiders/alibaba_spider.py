# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: alibaba.py 
@time: 2018/1/30 13:36 
"""

# encoding: utf-8

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: alibaba.py 
@time: 2018/1/30 13:45 
"""

import scrapy
import re
import json

from chouqian.items import AlibabaItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class AlibabaSpider(scrapy.Spider):
    print 'alibaba start'
    name = "alibaba"  # 唯一标识
    # allowed_domains = ["csdn.net"]
    start_urls = [
        "http://www.alibaba.com/Products?spm=a2700.8293689.201703.9.CsCxb0",

    ]

    #def start_requests(self): #测试cookie
    #    # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
    #    yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies={'meng':1})

    def parse(self, response):
        category_urls = response.xpath('//div[@class="sub-item"]//li/a/@href').extract()
        for url in category_urls:
            yield scrapy.Request(url = url,callback=self.parser_category)#没有callback默认就还是这个


    def parser_category(self,response):
        items_url = response.xpath('//div[@class="item-img"]//div[@class="util-valign img-wrap"]/a/@href').extract()
        for item_url in items_url:
            yield scrapy.Request(url=item_url, callback=self.parser_item)

    def parser_item(self,response):
        title = response.xpath('//h1/@title').extract_first()
        QuickDetails = response.xpath("//div[@class='do-entry-list']//dl").extract()
        detail = '\\1'.join(QuickDetails).replace('\n','')
        detail = re.sub('<.*?>','',detail)
        content = response.body
        path = []
        pathlistdict = re.search('(\{"pathList":\s*\[.*?\]\})', content.replace('\n','')).group(1)
        pathlists = json.loads(pathlistdict)["pathList"]
        for pathlist in pathlists:
            catname = pathlist.get('catName','')
            catid = pathlist.get('catId',0)
            path.append({'catName':catname,'catid':catid})

        item = AlibabaItem()
        item['title'] = title
        item['QuickDetails'] = detail
        item['category'] = str(path)
        item['url'] = response.url
        item['category_id'] = pathlists[-1].get('catId',0)


        yield item
