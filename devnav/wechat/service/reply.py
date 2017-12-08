# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: reply.py 
@time: 2017/12/1 14:37 
"""
from ..models import Reply,Resource,Resource_Cache
from django.db.models import Sum, Count,Avg
import logging
import datetime
from ..crawler.mainprocess import keywordSearch

logger = logging.getLogger('default')

def reply(MsgContent,userOpenId=''):
    queryResult = search_resource(MsgContent,userOpenId)
    if queryResult:#这个逻辑后面得改，不兼容搜索，要么就是根据公众号类型不同返回
       return {'reply': queryResult, 'mode': 0}
    #如果有资源就返回资源，如果没有就骂人 ,切换模式，模式需要在用户session中记录 输入别骂了才能切换回来 或者设置资源的前缀，不合法的都骂
    #reply = maRen()
    reply = crawler(MsgContent,userOpenId=userOpenId)
    if reply:
        return {'reply':reply,'mode':0}
    else:
        return {'reply':'出bug啦！！估计是网速不行，毕竟服务器不在国内，重试下吧','mode':1}

import random

#骂人回复
def maRen():
    results = Reply.objects.order_by("-weight").all()[:100]
    replys = []
    for result in results:
        reply = result.reply
        weight = result.weight
        replys.append([reply, weight])
    reply = weight_choice(replys)
    return reply

#爬虫回复
def crawler(keyword,userOpenId=''):
    rsDict = keywordSearch(keyword,sites=[19])
    urlinfos = rsDict['urlinfos']
    rs = []
    for urlinfo in urlinfos:
        title = urlinfo.get('title','')
        url = urlinfo.get('url','')
        rs.append("%s %s"%(title,url))
        if title and url:
            save_resource(title,url,keyword,userOpenId=userOpenId)

    result =  '\n'.join(rs)[:590]  #限制貌似是不能超过2048字节
    crawlerReply = ''
    strSum = 0
    for s in result:
        if s.isdigit()|s.isalpha()|s.c.isspace():strSum+=1
        else:strSum+=4
        crawlerReply = crawlerReply + s
        if strSum >2000:break
    #logger.debug(result)
    return crawlerReply


#带权重随机
def weight_choice(list):
    """
    #list = [['a',1],['b',1]]
    """
    sum=0
    for item in list:
        weight = item[1]
        sum+=weight
    choiceInt = random.randint(1,sum)
    sumChoice=0
    for item in list:
        weight = item[1]
        value = item[0]
        sumChoice+=weight
        if sumChoice>= choiceInt:
            return value

def search_resource(queryString,userOpenId=''):
    try:
        now = datetime.datetime.now()
        start = now-datetime.timedelta(hours=23, minutes=59, seconds=59)#缓存一天的数据
        resources = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=queryString)[:10]#后面需要加更多限制 反正也显示不了10条
        result=[]
        for resource in resources:
            result.append(resource.title + ' '+resource.url)
        output = '\n'.join(result)
    except Exception,e:
        logger.error(str(e))
    return output

def save_resource(title,url,keyword,userOpenId='',uploader='system'):
    try:
        r = Resource_Cache()
        r.title=title
        r.url = url
        r.keyword = keyword
        r.uploader = uploader
        r.OpenID = userOpenId
        r.create_time = datetime.datetime.now()
        r.save()
    except Exception,e:
        logger.error(str(e))