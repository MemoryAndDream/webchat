# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: testProcess.py 
@time: 2017/12/15 17:30 
"""

from  wechat.crawler.mainprocess import keywordSearch

re =  keywordSearch('权力的游戏 第二季', sites=[30, 31], sitesType='netDiskSites')['urlinfos']
for i in re:
    print i['title']