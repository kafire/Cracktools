#coding:utf-8

import os
import sys
import time
import socket
import ftplib
import poplib
import pymssql
import MySQLdb
import urlparse
import logging
import paramiko
import threading
from Queue import Queue


reload(sys)
sys.setdefaultencoding('utf-8')

socket.setdefaulttimeout(10)

mutex = threading.Lock()

path = os.path.join(__file__,'log.txt')



try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

cracks={
    "ftp":[("ftp","123"),("ftp","123456"),("ftp","ftp"),("test","test"),
           ("test","123456"),("test","123456"),("test","test"),("test","123"),
           ("test","test123"),("test","test123456")],
    "mysql":[("root","root"),("root",""),("test","123456"),
           ("test","123456"),("test","test"),("test","123"),
           ("test","test123"),("test","test123456")],
    "mssql":[("sa","sa"),("sa","123456"),("sa","root"),("test","123456"),
           ("test","123456"),("test","test"),("test","123"),
           ("test","test123"),("test","test123456")],
    "ssh":[("root","123456"),("root","root"),("root","123"),
           ("root","root123"),("root","root123456"),("test","123456"),
           ("test","123456"),("test","test"),("test","123"),
           ("test","test123"),("test","test123456")],
    "pop3":[("ftp","ftp"),("root","ftp"),("test","123456"),
           ("test","123456"),("test","test"),("test","123"),
           ("test","test123"),("test","test123456")],
    }

dicts = []
userlist = ["root",'ftp','sa']
pwdlist = ["root",'ftp']


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func
    def run(self):
        self.func()


class Engine(object):
    def __init__(self):
        self.userlist=["root"]
        self.pwdlist=["root"]


    def println(self,host,port,user=None,pwd=None):
        mutex.acquire()
        print host + ":" + port, user + ":" + pwd
        mutex.release()


    def ftp(self,host,port):
        crack=cracks.get("ftp")
        if crack:
            for user,pwd in crack:
                ftp = ftplib.FTP()
                try:
                    ftp.connect(host,int(port))
                except Exception as e:
                    break
                try:
                    ftp.login("anonymous","anonymous")
                    self.println( host, port,"anonymous","anonymous")
                    ftp.close()
                    break
                except ftplib.error_perm as e:
                    try:
                        ftp.login(user,pwd)
                        self.println(host, port,user,pwd)
                        ftp.close()
                        break
                    except Exception:
                        continue


    def mssql(self,host,port):
        crack = cracks.get("mssql")
        server = '%s:%s' % (host, int(port))
        if crack:
            for user,pwd in crack:
                try:
                    pymssql.connect(host=server,user=user, password=pwd,database= "master")
                    self.println(host, port, user, pwd)
                except Exception as e:
                    if "Server is unavailable" in str(e):
                        break
                    elif "Server connection failed" in str(e):
                        continue
                    else:
                        break


    def mysql(self,host,port):
        crack = cracks.get("mysql")
        if crack:
            for user,pwd in crack:
                try:
                    conn=MySQLdb.connect(host=host, port=int(port), user=user, passwd=pwd, db="mysql", connect_timeout=30)
                    self.println(host, port, user, pwd)
                    conn.close()
                except Exception as e:
                    if "Connection refused" in str(e):
                        break
                    elif 'Access denied' in str(e):
                        continue
                    else:
                        break


    def ssh(self,host,port):
        crack = cracks.get("ssh")
        if crack:
            for user,pwd in crack:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, int(port), user, pwd)
                    self.println(host, port, user, pwd)
                except paramiko.ssh_exception.AuthenticationException as e:
                    continue
                except Exception as e:
                    break



    def pop3(self,host,port):
        crack = cracks.get("pop3")
        if crack:
            for user,pwd in crack:
                try:
                    Mailbox = poplib.POP3(host, int(port))
                    Mailbox.user(user)
                    Mailbox.pass_(pwd)
                    self.println(host, port, user, pwd)
                    Mailbox.quit()
                except poplib.error_proto, e:
                    continue
                except Exception as e:
                    break


class Hydra():

    def __init__(self):
        self.targets=[]
        self.tasks_queue = Queue()


    def get_targets(self,_file, uri):
        if _file:
            for i in [x.strip() for x in file(_file, 'r')]:
                obj=urlparse.urlparse(i)
                scheme=obj.scheme
                netloc=obj.netloc
                self.targets.append((scheme, netloc))
        if uri:
            obj = urlparse.urlparse(uri)
            scheme = obj.scheme
            netloc = obj.netloc
            self.targets.append((scheme, netloc))
        return len(set(self.targets))


    def get_crack(self,userlist,pwdlist):
        for u in userlist:
            for p in pwdlist:
                dicts.append((u,p))
        return set(dicts)



    def engines(self,func,host,port):
        obj=Engine()
        func=getattr(obj,func)
        return func(host,port)



    def worker(self):
        while self.tasks_queue.qsize() > 0:
            target=self.tasks_queue.get(timeout=0.1)
            func,host,port=target
            self.engines(func,host,port)


    def monitor(self):
        while not self.tasks_queue.empty():
            print "{} tasks waiting...".format(self.tasks_queue.qsize())
            time.sleep(30)


    def scan(self,_file,netloc,thread=2):
        threads=[]
        print "Now start scaning....."
        self.get_targets(_file, netloc)
        self.get_crack(userlist,pwdlist)
        for scheme,netloc in self.targets:
            host,port=netloc.split(":")
            self.tasks_queue.put((scheme,host,port))
        print "Total has %s records to checking..." % (self.tasks_queue.qsize())
        for i in xrange(thread):
            thread = MyThread(self.worker)
            thread.start()
            threads.append(thread)
        self.monitor()
        for thread in threads :
            thread.join()



if __name__=="__main__":
    hd=Hydra()
    hd.scan(_file="test.txt",netloc=None)
