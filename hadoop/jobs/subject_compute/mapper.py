#!/usr/bin/env python
#coding:utf-8
import random
import os,sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

for line in sys.stdin:
    line = line.strip()
    f = line.split('')
    if len(f) != 6:
        continue
    content = f[2]
    cls = f[1]
    id = f[0]
    source = f[3]
    update_time = f[4]
    taskid = f[5]
    try:
        result = json.loads(content)
        #if result.get('subject', cls) == u'动漫':
        print '%s\t%s' % (result.get('subject') or cls, result.get('url') or '')
    except Exception as e:
        pass
