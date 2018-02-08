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
    url = 'https://so.360kan.com/index.php?kw=%s&from=' % (keyword)
    #print url
    urlinfos=[]
    page = ct.crawlerTool.getPage(url)
    if 'class="b-mainpic"' in page:
        detailsPage = ct.crawlerTool.getXpath('//div[@class="b-mainpic"]/a/@href', page)[0]
        detailsPageData = ct.crawlerTool.getPage(detailsPage)
        #tv
        aLevelTitle = ct.crawlerTool.getXpath('//div[@class="title-left g-clear"]/h1/text()',detailsPageData)[0]
        segments = ct.crawlerTool.getXpath('//div[@class="num-tab-main g-clear js-tab"]/a',detailsPageData)
        if segments:
            for segment in segments:
                try:
                    urlinfo={}
                    localurl=ct.getXpath('//a/@href',segment)[0]
                    if localurl:
                        if 'youku' in localurl and 'url=' in localurl:
                            localurl = ct.getRegex('url=(.*?html)&', localurl)
                        else:
                            localurl = localurl.split('?')[0]
                        #if 'qq' in localurl:
                        #    localurl='http://www.82190555.com/index/qqvod.php?url=' + localurl
                        #elif 'iqiyi' in localurl:
                        #    localurl='http://mlxztz.com/player.php?url='+localurl
                        #else:
                        #    localurl='http://api.baiyug.cn/vip/index.php?url=' + localurl
                        urlinfo['url']='http://www.85105052.com/admin.php?url=' +  localurl
                        #urlinfo['url']='http://api.baiyug.cn/vip/index.php?url=' + localurl
                        title =HTMLParser().unescape(ct.getXpath('//a/text()',segment)[0]).replace('\r\n','')
                        urlinfo['title'] = aLevelTitle+' '+title.strip()
                        if title == '收起':continue
                        urlinfos.append(urlinfo)
                    else:
                        pass
                except:
                    pass
            return {"urlinfos": urlinfos}
        # zongyi
        segments = ct.crawlerTool.getXpath('//div[@class="js-month-tab"]/ul/li', detailsPageData)
        #print segments
        if segments:
            for segment in segments:
                try:
                    urlinfo = {}
                    localurl = ct.getXpath('//li/a/@href', segment)[0]
                    if localurl:
                        if 'youku' in localurl and 'url=' in localurl:
                            localurl = ct.getRegex('url=(.*?html)&', localurl)
                        else:
                            if '?' in localurl:
                                localurl = ct.getRegex('(http.*?)\?',localurl)
                            else:
                                localurl =localurl
                        #if 'qq' in localurl:
                        #    localurl='http://www.82190555.com/index/qqvod.php?url=' + localurl
                        #elif 'iqiyi' in localurl:
                        #    localurl='http://mlxztz.com/player.php?url='+localurl
                        #else:
                        #    localurl='http://vip.thxcw.com/api.php?url=' + localurl
                        #print '++++++++++++++++++++++++',segment
                        urlinfo['url'] ='http://tv.x-99.cn/api/wnapi.php?id='+localurl
                        #urlinfo['url']='http://api.baiyug.cn/vip/index.php?url=' + localurl
                        title = HTMLParser().unescape(ct.getRegex('title="(.*?)"', segment))
                        titleId= ct.getRegex(u'第(\d+)期',title)
                        if titleId == '':
                            titleId =  ct.getRegex(u'>([\d-]+)期<',HTMLParser().unescape(ct.getXpath('//span[@class="w-newfigure-hint"]',segment)[0])).replace('-','')
                            #print titleId
                        urlinfo['title'] = title.strip()+' '+titleId
                        urlinfos.append(urlinfo)
                    else:
                        pass
                except:
                    pass
            return {"urlinfos": urlinfos}

        #movie
        segments = ct.crawlerTool.getXpath("/html/body/div[2]/div[1]/div[1]",page)
        #print segments
        if segments:
            for segment in segments:
                try:
                    #print segment
                    urlinfo={}
                    localurl=ct.getXpath('//div[@class="button-container g-clear"]/div[1]/a/@href',segment)[0]
                    if 'youku' in localurl and 'url=' in localurl:
                        localurl = ct.getRegex('url=(.*?html)&', localurl)
                    else:
                        if '?' in localurl:
                            localurl = ct.getRegex('(http.*?)\?',localurl)
                        else:
                            localurl = localurl
                    # print localurl
                    if localurl:
                        #if 'qq' in localurl:
                        #    localurl='http://www.82190555.com/index/qqvod.php?url=' + localurl
                        #elif 'iqiyi' in localurl:
                        #    localurl='http://mlxztz.com/player.php?url='+localurl
                        #else:
                        #    localurl='http://api.baiyug.cn/vip/index.php?url=' + localurl
                        urlinfo['url']= 'http://tv.x-99.cn/api/wnapi.php?id=' + localurl
                        #urlinfo['url']='http://api.baiyug.cn/vip/index.php?url=' + localurl
                        urlinfo['title'] =  HTMLParser().unescape(ct.getXpath('//div[@class="b-mainpic"]/a/@title',segment)[0])
                        urlinfos.append(urlinfo)
                    else:
                        pass
                except:
                    pass
            return {"urlinfos": urlinfos}

    else:
        urls = 'http://www.yingdou.net/search/index?key=%s' % (keyword)
        # print url
        urlinfos = []
        pages = ct.crawlerTool.getPage(urls)
        detailsPage1 = ct.crawlerTool.getXpath('//div[@class="movie-item"]/a/@href', pages)[0]
        details_PageData = ct.crawlerTool.getPage('http://www.yingdou.net' + str(detailsPage1))
        # tv
        aLevelTitle1 = ct.crawlerTool.getXpath('//div[@class="col-md-12"]/h1/text()', details_PageData)[0]
        segments = ct.crawlerTool.getXpath('//div[@class="panel panel-default resource-list"]/ul/li/a', details_PageData)
        if segments:
            # print 1
            for segment in segments:
                try:
                    urlinfo = {}
                    localurl = ct.getXpath('//a/@href', segment)[0]
                    if localurl:
                        localurl = 'http://www.yingdou.net' + str(localurl)
                        localurlpage = ct.crawlerTool.getPage(localurl)

                        title1 = ct.crawlerTool.getRegex(u'movie-title">视频名称：(.*?)\(', localurlpage)
                        titleNum = ct.crawlerTool.getRegex(u'第(\d+)集', title1)
                        pageurl = ct.crawlerTool.getXpath('//div[@class="player"]/iframe/@src', localurlpage)[0]
                        urlinfo['url'] = pageurl
                        title = HTMLParser().unescape(title1).replace('\r\n', '')
                        urlinfo['title'] = aLevelTitle1.strip() + ' ' + titleNum
                        urlinfos.append(urlinfo)

                    else:
                        pass
                except:
                    pass
            return {"urlinfos": urlinfos}


if __name__=='__main__':
    result = process("小美好",1)
    print result
