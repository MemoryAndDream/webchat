# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: 360kan.py 
@time: 2017/12/12 17:38 
"""
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback

def process(keyword,page):
    print keyword
    url = 'https://so.360kan.com/index.php?kw=%s&from=' % (keyword)
    print url
    urlinfos=[]
    page = ct.crawlerTool.getPage(url)
    #tv
    segments = ct.crawlerTool.getXpath("/html/body/div[2]/div[1]/div[1]/div[3]/div/div[2]/div/div//div[@class='b-series-number-container g-clear']/a",page)
    if segments:
        for segment in segments:
            try:
                #print segment
                urlinfo={}
                localurl=ct.getRegex('(http.*?)\?', ct.getXpath('//a/@href',segment)[0])
                if localurl:
                    urlinfo['url']= "http://api.baiyug.cn/vip/index.php?url=" + localurl
                    urlinfo['title'] =  HTMLParser().unescape(ct.getXpath('//a/text()',segment))
                    urlinfos.append(urlinfo)
                else:
                    pass
            except:
                pass
        return {"urlinfos": urlinfos}
    #movie
    segments = ct.crawlerTool.getXpath("/html/body/div[2]/div[1]/div[1]",page)
    print segments
    if segments:
        for segment in segments:
            try:
                #print segment
                urlinfo={}
                localurl=ct.getRegex('(http.*?)\?', ct.getXpath('//div[@class="button-container g-clear"]/div[1]/a/@href',segment)[0])
                if 'youku' in localurl and 'url=' in localurl:
                    localurl = ct.getRegex('url=(.*?html)&', localurl)
                else:
                    localurl = localurl
                # print localurl
                if localurl:
                    urlinfo['url']= "http://api.baiyug.cn/vip/index.php?url=" + localurl
                    urlinfo['title'] =  HTMLParser().unescape(ct.getXpath('//div[@class="b-mainpic"]/a/@title',segment))
                    urlinfos.append(urlinfo)
                else:
                    pass
            except:
                pass
        return {"urlinfos": urlinfos}



if __name__=='__main__':
    result = process("英伦对决",1)
    print result