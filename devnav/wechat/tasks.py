# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: tasks.py 
@time: 2017/12/19 10:39 
"""

from celery.decorators import task
from celery.utils.log import get_task_logger
import time
import datetime
from .models import Resource_Cache

logger = get_task_logger(__name__)

@task(name="wechat.save_resource_task")#唯一的name，不给会自动生成
def save_resource_task(title,url,keyword,userOpenId='',uploader='system'):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return save_resource(title,url,keyword,userOpenId='',uploader='system')


def wrapfunc(func):
    def wrapped_func(*args, **kwargs):
        start = time.time()
        while True:
            try:
                ret = func(*args, **kwargs)
                logger.debug("%s cost [%s]s, " % (func.__name__, time.time() - start))
                return ret
            except Exception, e:
                logger.error(str(e))
    return wrapped_func

@wrapfunc
def save_resource(title,url,keyword,userOpenId='',uploader='system'):

    r = Resource_Cache.objects.get_or_create(keyword=keyword,url=url,OpenID=userOpenId)[0]#一个用户的同一搜索只能存一条
    r.title=title
    r.uploader = uploader
    r.create_time = datetime.datetime.now()
    r.save()