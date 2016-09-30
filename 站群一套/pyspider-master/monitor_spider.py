#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import commands

content = commands.getoutput('tail -n 10 nohup.out')
if u'ResponseError:' in content:
                os.system('sh kill.sh')
                os.system('sh start.sh')
                print 'reload spider',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
else:
	start =  os.path.getsize('nohup.out')
	time.sleep(100)
	end = os.path.getsize('nohup.out')
	if start == end:
		os.system('sh kill.sh')
		os.system('sh start.sh')
		print 'reload spider',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

