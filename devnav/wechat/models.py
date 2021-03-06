# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

#ORM真tm难用！

class Reply(models.Model):
    reply = models.CharField(max_length=100)
    weight = models.IntegerField()
    update_time = models.DateTimeField('events time',blank=True)
    create_time = models.DateTimeField(blank=True)  # 创建时间(自动获取当前时间)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.reply

class Resource(models.Model):
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    post_date =  models.CharField(max_length=255,blank=True)
    request_count=  models.IntegerField(default=1)
    download_url = models.CharField(max_length=255,blank=True)
    update_time = models.DateTimeField('events time',blank=True)
    create_time = models.DateTimeField(blank=True)  # 创建时间(自动获取当前时间)
    verify_time = models.DateTimeField('verify time',blank=True)
    user = models.CharField(max_length=100,blank=True)#对应api的
    uploader = models.CharField(max_length=100,blank=True)#对应api的
    type = models.CharField(max_length=100, blank=True)#以,分割各种类型
    OpenID = models.CharField(max_length=100, blank=True)
    UnionID = models.CharField(max_length=100, blank=True)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.url+self.title

class User(models.Model):
    name = models.CharField(max_length=100, blank=True,null=True,default=None)
    OpenID = models.CharField(max_length=100, blank=True)
    UnionID = models.CharField(max_length=100, blank=True,null=True,default=None)
    last_input = models.CharField(max_length=100, blank=True,null=True,default=None)
    keyword = models.CharField(max_length=100, blank=True,null=True,default=None)
    last_page = models.IntegerField(default=1, blank=True,null=True)
    last_request_time = models.DateTimeField(auto_now=True,blank=True,null=True,default=None)

class Resource_Cache(models.Model):
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    post_date =  models.CharField(max_length=255,blank=True,null=True,default=None)
    request_count=  models.IntegerField(default=1,null=True)
    download_url = models.CharField(max_length=255,blank=True,null=True,default=None)
    update_time = models.DateTimeField('events time',blank=True,null=True,default=None)
    create_time = models.DateTimeField(blank=True,null=True,default=None,db_index=True)  # 创建时间(自动获取当前时间)
    verify_time = models.DateTimeField('verify time',blank=True,null=True,default=None)
    user = models.CharField(max_length=100,blank=True,null=True,default=None)#对应api的
    uploader = models.CharField(max_length=100,blank=True,null=True,default=None)#对应api的
    type = models.CharField(max_length=100, blank=True,null=True,default=None)#以,分割各种类型
    OpenID = models.CharField(max_length=100, blank=True,null=True,default=None)
    UnionID = models.CharField(max_length=100, blank=True,null=True,default=None)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.url+self.title

class CouQian(models.Model):
    OpenID = models.CharField(max_length=100, blank=True,null=True,unique=True)
    qian_id = models.IntegerField(blank=True,null=True,default=0)

class Qian(models.Model):
    title = models.CharField(max_length=100,blank=True,default=None)
    img_url = models.CharField(max_length=255,blank=True,null=True,default=None)
    page_url = models.CharField(max_length=255,blank=True,null=True,default=None)
    type = models.CharField(max_length=20,blank=True,null=True,default=None)
    detail = models.TextField(blank=True,null=True,default=None) #null=True表示建表时该字段可以为空