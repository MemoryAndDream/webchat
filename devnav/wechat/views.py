# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import sys
reload(sys)
sys.setdefaultencoding('utf8')   
from service.reply import reply
from service.learn import learn
import logging
logger = logging.getLogger('default')

#django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #服务器配置中的token
        token = 'mengzaizai'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("failed")
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)

#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET
def autoreply(request):

    try:
        webData = request.body
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text
        MsgContent = xmlData.find('Content').text



        toUser = FromUserName#用户openid
        fromUser = ToUserName#微信公众号的openid
        #print MsgContent
        if msg_type == 'text':
            #print MsgContent
            logger.info('in:'+str(MsgContent))

            if MsgContent.startswith('s='):
                learnContent = MsgContent[2:].split('w=')
                if len(learnContent)>1:
                    replyContent = learn(learnContent[0],learnContent[1])
                else:replyContent = learn(learnContent[0])
            if fromUser == 'gh_af4058d792a2':#abc快看
                replyContent = reply(MsgContent=MsgContent, userOpenId=toUser, mod='qgg')['reply']
            else:
                import re
                if  re.match('\d+',MsgContent):
                    replyContent = reply(MsgContent=MsgContent, userOpenId=toUser, mod='qgg')['reply']
                elif MsgContent.startswith('qgg '):
                    keyword = MsgContent[4:]
                    replyContent = reply(MsgContent=keyword, userOpenId=toUser,mod='qgg')['reply']
                elif MsgContent :
                    replyContent = reply(MsgContent=MsgContent,userOpenId=toUser)['reply']#传入用户的openid？
                    #print 'shucu'
                else:
                    replyContent = "这公众号傻逼了"
            logger.info('out:' + str(replyContent))
            replyMsg = TextMsg(toUser, fromUser, replyContent)
            #print "成功了!!!!!!!!!!!!!!!!!!!"
            #print replyMsg
            return replyMsg.send()
        elif MsgType == 'event':
            Event  = xmlData.find('Event').text
            #订阅事件
            if Event == 'subscribe':
                if fromUser == 'gh_af4058d792a2':
                    content = "欢迎订阅本公众号，输入资源名 搜索并获取各大视频网站免会员去广告视频入口"
                else:
                    content = "欢迎订阅本公众号，输入资源名查询百度云资源，输入qgg 资源名 获取各大视频网站免会员去广告视频入口" \
                          "搜索时请具体一些，比如权力的游戏 第六季 或qgg 爱情公寓4"
                replyMsg = TextMsg(toUser, fromUser, content)
                logger.info('login: from'+str(FromUserName)+' to '+str(ToUserName))
                return replyMsg.send()

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()


        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception, Argment:
        logger.error(str(Argment))
        return Argment

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
