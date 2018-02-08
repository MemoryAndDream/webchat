# encoding: utf-8

"""
@author: Meng.ZhiHao
@contact: 312141830@qq.com
@file: 360kan.py
@time: 2017/12/12 17:38
"""
from ..common import  crawlerTool as ct
#import  crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback

def process(keyword,page):
    #print keyword
    url = 'http://www.yingdou.net/search/index?key=%s' % (keyword)
    #print url
    urlinfos=[]
    page = ct.crawlerTool.getPage(url)
    detailsPage = ct.crawlerTool.getXpath('//div[@class="movie-item"]/a/@href', page)[0]
    detailsPageData = ct.crawlerTool.getPage('http://www.yingdou.net'+str(detailsPage))
    #tv
    aLevelTitle = ct.crawlerTool.getXpath('//div[@class="col-md-12"]/h1/text()',detailsPageData)[0]
    segments = ct.crawlerTool.getXpath('//div[@class="panel panel-default resource-list"]/ul/li/a',detailsPageData)
    if segments:
        #print 1
        for segment in segments:
            try:
                urlinfo={}
                localurl=ct.getXpath('//a/@href',segment)[0]
                if localurl:
                    localurl='http://www.yingdou.net'+str(localurl)
                    localurlpage = ct.crawlerTool.getPage(localurl)

                    title1 = ct.crawlerTool.getRegex(u'movie-title">视频名称：(.*?)\(',localurlpage)
                    titleNum = ct.crawlerTool.getRegex(u'第(\d+)集',title1)
                    pageurl=ct.crawlerTool.getXpath('//div[@class="player"]/iframe/@src',localurlpage)[0]
                    urlinfo['url'] = pageurl
                    title = HTMLParser().unescape(title1).replace('\r\n', '')
                    urlinfo['title'] = aLevelTitle.strip()+ ' ' +titleNum
                    urlinfos.append(urlinfo)

                else:
                    pass
            except:
                pass
        return {"urlinfos": urlinfos}
