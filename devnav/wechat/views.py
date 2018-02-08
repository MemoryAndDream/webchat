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
#from service.reply import reply
from service.reply_new import reply,chou_qian
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
            logger.info('in:'+str(toUser)+' '+str(MsgContent))
            if MsgContent.endswith('保佑'):
                title, description, picurl, url = chou_qian(userOpenId=toUser)
                replyMsg = PicTextMsg(toUser, fromUser, title,description,picurl,url)

                return replyMsg.send()
            if MsgContent.startswith('s='):
                learnContent = MsgContent[2:].split('w=')
                if len(learnContent)>1:
                    replyContent = learn(learnContent[0],learnContent[1])
                else:replyContent = learn(learnContent[0])
            if MsgContent.startswith('pan'):
                if MsgContent.startswith('pan '):keyword = MsgContent[4:]
                else: keyword = MsgContent[3:]
                replyContent = reply(MsgContent=keyword, userOpenId=toUser, mod='pan')['reply']
            else:
                replyContent = reply(MsgContent=MsgContent, userOpenId=toUser, mod='qgg')['reply']

            logger.info('out:' +str(toUser)+' '+ str(replyContent))
            replyMsg = TextMsg(toUser, fromUser, replyContent)
            #print "成功了!!!!!!!!!!!!!!!!!!!"
            #print replyMsg
            return replyMsg.send()
        elif MsgType == 'event':
            Event  = xmlData.find('Event').text
            #订阅事件
            if Event == 'subscribe':
                content = "欢迎订阅本公众号，输入资源名 搜索并获取各大视频网站免会员去广告视频入口"
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


class PicTextMsg(Msg): # 只发一条图文消息
    def __init__(self, toUserName, fromUserName, title,description,picurl,url):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['title'] = title
        self.__dict['description'] = description
        self.__dict['picurl'] = picurl
        self.__dict['url'] = url

    def send(self):
        xmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item><Title><![CDATA[{title}]]></Title> 
        <Description><![CDATA[{description}]]></Description>
        <PicUrl><![CDATA[{picurl}]]></PicUrl>
        <Url><![CDATA[{url}]]></Url>
        </item>
        </Articles></xml>
        """
        logger.info(xmlForm.format(**self.__dict))
        return xmlForm.format(**self.__dict)

def reply_test(request):
    if request.method == "GET":
        input = request.GET.get('input', '')
        mod = request.GET.get('mod', 'qgg')
        userOpenId = request.GET.get('userOpenId', 'okohewlbCCuGpCoYL0idJlOVDY7o')

        replyContent = reply(MsgContent=input, userOpenId=userOpenId, mod=mod)['reply']
        return HttpResponse(replyContent)
