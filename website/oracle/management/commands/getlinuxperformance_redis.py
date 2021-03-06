#coding=utf-8
#coding=gbk
from django.core.management.base import BaseCommand
from oracle.models import linuxlist
import os
import redis
import time
from time import ctime,sleep
import threading
from oracle.monitor.getlinuxinfo import *
from oracle.monitor.sendmail import *
class Command(BaseCommand):
    def handle(self, *args, **options):
	def getperformance(i):
	    if i.performance_type==1:
		    ipaddress=i.ipaddress
		    username=i.username
		    password=i.password
		    hostname1=i.hostname
		    try:
			if i.os=='linux':
			    ssh = paramiko.SSHClient()
			    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			    ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
			    linuxcpu=getlinuxcpu(ssh)
			    linuxmem=getlinuxmem(ssh)
			    ssh.close()
			    dskey='CPU='+ipaddress+'='+hostname1
			    value=nowtime+':'+ str(linuxcpu)
			    r.lpush(dskey,value)
			    dskey='MEMORY='+ipaddress+'='+hostname1
			    value=nowtime+':'+ str(linuxmem)
			    r.lpush(dskey,value)
#			    print ipaddress+hostname1
			else:
			    ssh = paramiko.SSHClient()
			    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			    ssh.connect(hostname=ipaddress,port=22,username=username,password=password)
			    unixcpu=getunixcpu(ssh)
			    unixmem=getunixmem(ssh)
			    ssh.close()
			    dskey='CPU='+ipaddress+'='+hostname1
			    value=nowtime+':'+ str(unixcpu)
			    r.lpush(dskey,value)
			    dskey='MEMORY='+ipaddress+'='+hostname1
			    value=nowtime+':'+ str(unixmem)
			    r.lpush(dskey,value)
		    except Exception, e:
			result1=str(e)+ipaddress
			mailcontent.append(result1)
			print mailcontent
                    time.sleep(20)
	mailcontent=[]
	r=redis.StrictRedis()
	nowtime=str(time.time()).split('.')[0]
	ip=linuxlist.objects.all().order_by('ipaddress')
	threads=[]
	for i in ip:
	    t1 = threading.Thread(target=getperformance,args=(i,))
	    threads.append(t1)
        for t in threads:
            t.setDaemon(True)
            t.start()
	t.join()
	r.save()
