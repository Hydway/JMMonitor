# coding=utf-8

import requests,json,sys
from lxml import etree

class weiboMonitor():
    """
        @   Class self  :
    """
    def __init__(self, ):
        self.session = requests.session()
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #'Content-Type': 'application/x-www-form-urlencoded',
            #'Referer': 'https://passport.weibo.cn/signin/login',
            #'Connection': 'close',
            'Host': 'm.weibo.cn',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }

    """
        @   Class self  :
        @   String userName  : The username of weibo.cn
        @   String passWord  : The password of weibo.cn
    """
    def login(self, userName, passWord):
        loginApi = 'https://passport.weibo.cn/sso/login'
        loginPostData = {
            'username':userName,
            'password':passWord,
            'savestate':1,
            'r':'',
            'ec':'0',
            'pagerefer':'',
            'entry':'mweibo',
            'wentry':'',
            'loginfrom':'',
            'client_id':'',
            'code':'',
            'qq':'',
            'mainpageflag':1,
            'hff':'',
            'hfp':''
        }
        #get user session
        try:
            r = self.session.post(loginApi,data=loginPostData,headers=self.reqHeaders)
            if r.status_code == 200 and json.loads(r.text)['retcode'] == 20000000:
                self.echoMsg('Info','Login successful! UserId:'+json.loads(r.text)['data']['uid'])
            else:
                self.echoMsg('Error','Logon failure!')
                sys.exit()
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()

    """
        @   Class self  :
        @   String wbUserId  : The user you want to monitored
    """
    def getWBQueue(self, wbUserId):
        #get user weibo containerid
        userInfo = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s'%(wbUserId,wbUserId)
        try:
            r = self.session.get(userInfo,headers=self.reqHeaders)
            for i in r.json()['data']['tabsInfo']['tabs']:
                if i['tab_type'] == 'weibo':
                    conId = i['containerid']
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()
        #get user weibo index
        self.weiboInfo = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s&containerid=%s'%(wbUserId,wbUserId,conId)
        try:
            r = self.session.get(self.weiboInfo,headers=self.reqHeaders)
            self.itemIds = []   #WBQueue
            for i in r.json()['data']['cards']:
                if i['card_type'] == 9:
                    self.itemIds.append(i['mblog']['id'])
            self.echoMsg('Info','Got weibos')
            #self.echoMsg('Info','Has %d id(s)'%len(self.itemIds))
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()
    """
        @   Class self  :
    """
    def startMonitor(self):
        returnDict = {}
        try:
            r = self.session.get(self.weiboInfo,headers=self.reqHeaders)
            for i in r.json()['data']['cards']:
                if i['card_type'] == 9:
                    if str(i['mblog']['id']) not in self.itemIds:
                        self.itemIds.append(i['mblog']['id'])
                        self.echoMsg('Info','Got a new weibo')
                        #@ return returnDict dict
                        returnDict['created_at'] = i['mblog']['created_at']
                        returnDict['text'] = i['mblog']['text']
                        returnDict['source'] = i['mblog']['source']
                        returnDict['nickName'] = i['mblog']['user']['screen_name']
                        #if has photos
                        if 'pics' in i['mblog']:
                            returnDict['picUrls'] = []
                            for j in i['mblog']['pics']:
                                returnDict['picUrls'].append(j['url'])
                        return returnDict
            self.echoMsg('Info','Has %d id(s)'%len(self.itemIds))
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()

    """
        @   String level   : Info/Error
        @   String msg     : The message you want to show
    """
    def echoMsg(self, level, msg):
        if level == 'Info':
            print('[Info] %s'%msg)
        elif level == 'Error':
            print('[Error] %s'%msg)
