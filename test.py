# James Huang     uid = 6686767362
# https://m.weibo.cn/u/6686767362?uid=6686767362&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%BB%84%E4%BB%81%E8%BE%85%E7%90%86%E6%80%A7
#
# xiaoyu   uid =  6429975790
# https://m.weibo.cn/u/6429975790?uid=6429975790&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%AC%91%E5%AE%87%E4%B8%8E%E7%AC%91%E9%B1%BC

import new_weiboMonitor as wbm
import time,hashlib,requests

def main(uid):
    w = wbm.weiboMonitor()
    w.getWBQueue(uid)
    while 1:
        newWB = w.startMonitor()
        if newWB is not None:
            print newWB['text']
        time.sleep(600)

if __name__ == '__main__':
    uid= input('Please input the weibo user id you want to monitor : ')
    main(uid)
