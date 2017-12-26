# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: urls.py 
@time: 2017/11/29 17:14 
"""
from django.conf.urls import include, url
from django.contrib import admin
import views

app_name = 'wechat'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
url(r'^test/', views.reply_test, name='reply_test'),
    url(r'^$', views.weixin_main, name='weixin_main'),

    #url(r'^startmymenu$', views.startmymenu, name='startmymenu'),
    ]
