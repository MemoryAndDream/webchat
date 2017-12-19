# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: tasks.py 
@time: 2017/12/19 10:39 
"""

from celery.decorators import task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from service.reply import save_resource

@task(name="save_resource_task")
def save_resource_task(title,url,keyword,userOpenId='',uploader='system'):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return save_resource(title,url,keyword,userOpenId='',uploader='system')