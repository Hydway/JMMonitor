# coding=utf-8

import new_weiboMonitor as wbm
import time,hashlib,requests
import smtplib
import base64
import csv
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

def getMd5(str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()

def downloadImg(imgSrc):
    r = requests.get(imgSrc.strip())
    fileName = getMd5(imgSrc) + '.png'
    with open('images/' + fileName, 'wb') as f:
        f.write(r.content)
    return 'images/' + fileName

def sendMail(dicts):
    flag = True
    with open('mail_list.csv') as f:
        row = csv.reader(f, delimiter = '+')
        _user = next(row)[0]
        _pwd = next(row)[0]
        _to  = next(row)[0]
    try:
        text = u'发送时间: '+dicts['created_at']+u'<br>'
        text += u'发送内容: <br>'+dicts['text']+u'<br>'
        if 'picUrls' in dicts:
            for pic in dicts['picUrls']:
                imgFile = downloadImg(pic)
                f = open(imgFile, 'rb')
                baseCode = base64.b64encode(f.read())
                text += u'<img src="data:image/png;base64,%s">'%baseCode
        text += u'<br>来自: '+ dicts['source']

        msg=MIMEText(text.encode('utf-8'),'html','utf-8')
        msg['Form'] = formataddr(["微博监控系统", _user])
        msg['To'] = formataddr(["微博监控系统", _to])
        print(msg.as_string())
        server = smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(_user, _pwd)
        server.sendmail(_user, _to.split(), msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
        flag = False
    return flag

def main(uid):
    w = wbm.weiboMonitor()
    w.getWBQueue(uid)
    while 1:
        newWB = w.startMonitor()
        if newWB is not None:
            print(sendMail(newWB))
        time.sleep(10)

if __name__ == '__main__':
    uid= input('Please input the weibo user id you want to monitor : ')
    main(uid)

# James Huang     uid = 6686767362
# https://m.weibo.cn/u/6686767362?uid=6686767362&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%BB%84%E4%BB%81%E8%BE%85%E7%90%86%E6%80%A7
#
# xiaoyu   uid =  6429975790
# https://m.weibo.cn/u/6429975790?uid=6429975790&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%AC%91%E5%AE%87%E4%B8%8E%E7%AC%91%E9%B1%BC
