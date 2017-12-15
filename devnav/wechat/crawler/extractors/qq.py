# encoding: utf-8

"""
@author: Meng.ZhiHao
@contact: 312141830@qq.com
@file: qq.py
@time: 2017/12/12 17:38
"""
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback

def process(keyword,page):
    keywords=urllib.quote(keyword)
    url = 'https://v.qq.com/x/search/?q=%s' % (keywords)
    #print url
    urlinfos=[]
    page = ct.crawlerTool.getPage(url)
    dataId=ct.crawlerTool.getRegex('data-id="(\w+)"',page)
    apiurl = 'http://s.video.qq.com/get_playsource?id=%s&plat=2&type=4&data_type=2&video_type=3&range=0-100000&otype=json' % str(dataId)
    apiurlData = ct.crawlerTool.getPage(apiurl)
    aLevelTitle=ct.crawlerTool.getRegex("data-id=.*?r-props=\"[\D\d]*?title: '(.*?)';",page)
    apiUrlLists =ct.crawlerTool.getRegex('videoPlayList":(.*)\},"error',apiurlData)
    segments = re.findall('(\{.*?\})',apiUrlLists)
    if segments:
        for segment in segments:
            #print segment
            try:
                urlinfo={}
                print segment
                localurl=ct.crawlerTool.getRegex('playUrl":"(http.*?)"',segment)
                print localurl
                if localurl:
                    if 'youku' in localurl and 'url=' in localurl:
                        localurl = ct.getRegex('url=(.*?html)&', localurl)
                    elif 'iqiyi' in localurl:
                        localurl = ct.getRegex('(http.*?)\?',localurl)
                    elif 'mgtv' in localurl:
                        localurl = ct.getRegex('(http.*?)\?', localurl)
                    else:
                        localurl = localurl
                    urlinfo['url']= "http://api.baiyug.cn/vip/index.php?url=" + localurl
                    title =ct.crawlerTool.getRegex('title":"(.*?)"',segment)
                    urlinfo['title'] = aLevelTitle.replace('\x05','').replace('\x06','').strip()+' '+title.strip()
                    urlinfos.append(urlinfo)
                else:
                    pass
            except:
                pass
        return {"urlinfos": urlinfos}


if __name__=='__main__':
    result = process("明星大侦探",1)
    print result