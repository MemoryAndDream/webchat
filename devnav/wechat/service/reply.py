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
import time

from ..crawler.mainprocess import keywordSearch

logger = logging.getLogger('default')

def my_wrapfunc(func):
    def wrapped_func(*args, **kwargs):
        start = time.time()
        while True:
            try:

                ret = func(*args, **kwargs)
                logging.debug("%s cost [%s]s, " % (func.__name__, time.time() - start))
                return ret
            except Exception, e:
                logging.error(str(e))
    return wrapped_func

@my_wrapfunc
def reply(MsgContent,userOpenId='',mod=''):
    queryResult = search_resource(MsgContent,userOpenId,mod=mod)
    if queryResult:#这个逻辑后面得改，不兼容搜索，要么就是根据公众号类型不同返回
       return {'reply': queryResult, 'mode': 0}
    #如果有资源就返回资源，如果没有就骂人 ,切换模式，模式需要在用户session中记录 输入别骂了才能切换回来 或者设置资源的前缀，不合法的都骂
    #reply = maRen()
    if mod == 'qgg':
        reply = crawler(MsgContent, userOpenId=userOpenId,sites=[30],mod=mod)
    else:
        reply = crawler(MsgContent,userOpenId=userOpenId,sites=[19],mod=mod)
    if reply:
        return {'reply':reply,'mode':0}
    else:
        return {'reply':'没有搜到结果','mode':1}

import random

#骂人回复
@my_wrapfunc
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
@my_wrapfunc
def crawler(keyword,userOpenId='',sites=[19],mod=''):
    rsDict = keywordSearch(keyword,sites=sites)
    urlinfos = rsDict['urlinfos']
    rs = []
    for urlinfo in urlinfos:
        title = urlinfo.get('title','').replace("'",'"')
        url = urlinfo.get('url','')
        rs.append('''<a href='%s'>%s</a> '''%(url,title))
        if title and url:
            save_resource(title+'_'+mod,url,keyword,userOpenId=userOpenId)
    return results_toString(rs,mod)

@my_wrapfunc
def results_toString(rs,mod=''):  #限制貌似是不能超过2048字节
    crawlerReply = ''
    strSum = 0
    rs.reverse()#倒序排列 这操作会改变原来的数组
    for resultStr in rs:
        if strSum > 1970:
            if mod == 'qgg':
                crawlerReply = crawlerReply + '回复数字集数显示未显示集数'
            break
        for s in resultStr:
            if s.isdigit()|s.isalpha()|s.isspace():strSum+=1
            else:strSum+=4
            crawlerReply = crawlerReply + s
        crawlerReply = crawlerReply + '\n\n'
    return crawlerReply


#带权重随机
@my_wrapfunc
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

@my_wrapfunc
def search_resource(queryString,userOpenId='',mod=''):
    #这里增加一个逻辑 如果用户输入数字，则先去数据库里搜索最近一分钟title包含 数字_的结果 按时间倒序排列
    now = datetime.datetime.now()
    import re
    if re.match('\d+',queryString):
        start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        resources = Resource_Cache.objects.filter(OpenID__iexact=userOpenId).filter(create_time__gt=start).filter(title__endswith=' '+queryString + '_' + mod).order_by("-create_time")[:10]

    else:
        start = now-datetime.timedelta(hours=23, minutes=59, seconds=59)#缓存一小时的数据 读取缓存需要修改用户id  缓存和上面的逻辑有冲突
        resources = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=queryString+'_'+mod)[:10]#后面需要加更多限制 反正也显示不了10条
    result=[]

    for resource in resources:
        result.append('''<a href='%s'>%s</a> '''%(resource.url,resource.title.replace('_' + mod,'')))
        resource.create_time = now
        resource.OpenID = userOpenId#这个操作以后可以改成重新create一条
        resource.save()

    output = results_toString(result,mod)
    return output

@my_wrapfunc
def save_resource(title,url,keyword,userOpenId='',uploader='system'):
    r = Resource_Cache.objects.get_or_create(keyword=keyword,url=url,OpenID=userOpenId)[0]#一个用户的同一搜索只能存一条
    r.title=title
    r.uploader = uploader
    r.create_time = datetime.datetime.now()
    r.save()
