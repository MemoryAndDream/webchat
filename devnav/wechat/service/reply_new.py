# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: reply.py 
@time: 2017/12/1 14:37 
"""
from ..models import Reply,Resource,Resource_Cache,User,CouQian,Qian
from django.db.models import Sum, Count,Avg
import logging
import datetime
import time
#from celery import task
#from ..tasks import save_resource_task
from ..crawler.mainprocess import keywordSearch
from ..crawler.common.crawlerTool import crawlerTool as ct
import re
import random

logger = logging.getLogger('default')

def my_wrapfunc(func):
    def wrapped_func(*args, **kwargs):
        start = time.time()
        try:
            ret = func(*args, **kwargs)
            logger.debug("%s cost [%s]s, " % (func.__name__, time.time() - start))
            return ret
        except Exception, e:
            logger.error('func [%s] error [%s]'%(func.__name__,str(e)))
    return wrapped_func

@my_wrapfunc
def reply(MsgContent,userOpenId='',mod=''):
    start = time.time()
    save_input(userOpenId,MsgContent,mod=mod)
    logger.debug('input:%s userId:%s mod:%s'%(MsgContent,str(userOpenId),mod))
    if '看不了' in MsgContent:
        return {'reply': '如果播放失败请尝试重新打开链接，或者将问题留言在任意的推送文章中，我们会尽快修复，谢谢', 'mode': 0}
    if '优惠' in MsgContent:
        return {'reply': '''
淘宝优惠

精选淘宝/天猫最热门优惠券
￥mtxE0n4fDcz￥ 精选淘宝/天猫最热门优惠券，复制本段文字后打开淘宝领取

更多优惠收集中，有好的建议请留言,用户就是上帝！(◕ᴗ◕✿)''', 'mode': 0}
    queryResult = search_resource(MsgContent,userOpenId,mod=mod)
    if queryResult:#这个逻辑后面得改，不兼容搜索，要么就是根据公众号类型不同返回
       return {'reply': queryResult, 'mode': 0}
    #如果有资源就返回资源，如果没有就骂人 ,切换模式，模式需要在用户session中记录 输入别骂了才能切换回来 或者设置资源的前缀，不合法的都骂
    #reply = maRen()
    if mod == 'qgg':
        reply = crawler(MsgContent, userOpenId=userOpenId,sites=[30],mod=mod)
    elif mod == 'pan':
        reply = crawler(MsgContent, userOpenId=userOpenId,sites=[19],mod=mod)
    else:
        reply = crawler(MsgContent,userOpenId=userOpenId,sites=[19],mod=mod)
    if reply:
        return {'reply':reply,'mode':0}
    elif re.match('\s*\d+\s*$',MsgContent):
        return {'reply': '没有搜到对应集数 请重新搜索作品名称（不要带集数）', 'mode': 1}
   # elif mod and mod != 'pan':
    #    return {'reply': '没有搜到结果,你可以在标题前加上 pan 搜索云盘内容，如"pan 权力的游戏" ', 'mode': 1}
    elif time.time() - start >5:#这个不太灵，因为搜索可能就会超过6秒
        return {'reply': '处理超时了，重试一次吧亲', 'mode': 1}
    else:
        return {'reply':'没有搜到结果','mode':1}



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




def url_wraper(url):
    if '?' in url:
        url = url+'&rd=%s'%random.randint(0,999)
    else:
        url = url + '?rd=%s'%random.randint(0,999)
    return url


#爬虫回复
@my_wrapfunc
def crawler(keyword,userOpenId='',sites=[19],mod=''):
    rsDict = keywordSearch(keyword,sites=sites)
    urlinfos = rsDict['urlinfos']
    rs = []
    for urlinfo in urlinfos:
        title = urlinfo.get('title','').replace("'",'"')
        url = urlinfo.get('url','')
        rs.append('''<a href='%s'>%s</a> '''%(url_wraper(url),title))
        if title and url:
            #save_resource_task.delay(title+'_'+mod,url,keyword,userOpenId=userOpenId)  #异步发现不靠谱
            save_resource(title + '_' + mod, url, keyword+ '_' + mod, userOpenId=userOpenId)
    return results_toString(rs,mod)

@my_wrapfunc
def results_toString(rs,mod=''):  #限制貌似是不能超过2048字节
    crawlerReply = ''
    strSum = 0
    if mod == 'qgg':
        rs.reverse()#倒序排列 这操作会改变原来的数组
        pass
    for resultStr in rs:
        if strSum > 1970:
            if mod == 'qgg':
                crawlerReply = crawlerReply + '有未显示集数，回复数字集数(如 1)从第n集开始显示'
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

    if re.match('\s*\d+\s*$',queryString):
        queryString = queryString.replace(' ','')
        page = int(queryString)
        start = now - datetime.timedelta(hours=3, minutes=0, seconds=0)
        user = User.objects.filter(OpenID__iexact=userOpenId)
        if user: #利用user表保存keyword，防止异步 这里需要加个翻页的逻辑 后面用这种mod的模式不好
            user = user[0]
            keyword = user.keyword
            search_resource = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=keyword)
            logger.debug(keyword,search_resource)
            #.filter(title__endswith=' '+queryString + '_' + mod) 先拉出完整搜索结果存入数组
            rs_dict = {}
            resources=[]
            for r in search_resource:
                rs_page = ct.getRegex(" (\d+)_%s"%mod ,r.title)

                if rs_page:
                    rs_page=int(rs_page)
                    if rs_page >= page:
                        resources.append(r)
            resources.reverse()

        else:
            resources = Resource_Cache.objects.filter(create_time__gt=start).filter(OpenID__iexact=userOpenId).filter(title__endswith=' '+queryString + '_' + mod).order_by("-create_time")

    else:
        start = now-datetime.timedelta(hours=3, minutes=0, seconds=0)#缓存一天的数据 读取缓存需要修改用户id  缓存和上面的逻辑有冲突
        resources = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=queryString+'_'+mod) #应该显示不了30条吧

    result=[]

    for resource in resources:
        result.append('''<a href='%s'>%s</a> '''%(url_wraper(resource.url),resource.title.replace('_' + mod,'')))
        resource.OpenID = userOpenId#这个是有问题的
        resource.save()


    output = results_toString(result,mod)
    return output



@my_wrapfunc
def save_resource(title,url,input,userOpenId='',uploader='system'):
    logger.debug('save a record %s %s %s %s'%(title,url,input,userOpenId))
    r = Resource_Cache.objects.create(keyword=input,url=url,OpenID=userOpenId)#一个用户的同一搜索只能存一条
    r.title=title
    r.uploader = uploader
    r.create_time = datetime.datetime.now()
    r.save()


@my_wrapfunc
def save_input(userOpenId,input,mod=''):
    u=User.objects.get_or_create(OpenID=userOpenId)[0]

    u.last_input = input
    if not re.match('\s*\d+\s*',input):
        u.keyword = input+'_'+mod
    u.last_page = 1
    u.last_request_time = datetime.datetime.now()
    u.save()

@my_wrapfunc
def chou_qian (userOpenId,type='gy'): #可以选择抽签种类
    qian_id = 0
    r = CouQian.objects.get_or_create(OpenID=userOpenId)[0]
    if r.qian_id:
        qian_id = r.qian_id
    else:
        qians = Qian.objects.filter()
        qian_id = random.choice(qians).id
        r.qian_id = qian_id
        r.save()

    rs = Qian.objects.filter(id__iexact=qian_id)
    if rs:
        rs = rs[0]
        title = rs.title
        description = '新年求签'
        picurl = rs.img_url
        url = rs.page_url

    return title, description, picurl, url
