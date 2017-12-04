# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: reply.py 
@time: 2017/12/1 14:37 
"""
from ..models import Reply
from django.db.models import Sum, Count,Avg
def reply(MsgContent):

    #如果有资源就返回资源，如果没有就骂人 ,切换模式，模式需要在用户session中记录 输入别骂了才能切换回来 或者设置资源的前缀，不合法的都骂
    results = Reply.objects.order_by("-weight").all()[:100]
   # reply = results[0].reply
    #weights=Reply.objects.aggregate(Sum('weight'))
    replys=[]
    for result in results:
        reply = result.reply
        weight = result.weight
        replys.append([reply,weight])
    reply = weight_choice(replys)
    if reply:
        return {'reply':reply,'mode':0}
    else:
        return {'reply':'出bug啦！！','mode':1}

import random

#list = [['a',1],['b',1]]

def weight_choice(list):
    """
    :param weight: list对应的权重序列
    :return:选取的值在原列表里的索引
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