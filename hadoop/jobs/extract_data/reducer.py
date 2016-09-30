#!/usr/bin/env python
#ecoding:utf-8

import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
old_key = '0'
cnt = 0
_dict = {u'鼓':0}
for line in sys.stdin:
    try:
        line = line.strip()
        f = line.split('\t')
        if f[0]:
            #print '%s\t%s' % (f[0],f[1])
            if f[0]==u'鼓':
                if _dict[f[0]] == 10:
                    break
                print line
                _dict[f[0]] += 1
            else:
                pass
    except Exception as e:
        pass
