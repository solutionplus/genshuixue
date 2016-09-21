#!/usr/bin/env python
#ecoding:utf-8

import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
old_key = '0'
cnt = 0
_dict = {}
for line in sys.stdin:
    try:
        line = line.strip()
        f = line.split('\t')
        if '' not in f and len(f)==2:
            #print '%s\t%s' % (f[0],f[1])
            if _dict.has_key(f[0]):
                _dict[f[0]].add(f[1])
            else:
                _dict[f[0]] = set()
    except Exception as e:
        pass
for k,v in _dict.items():
    print '%s\t%s'%(k,','.join(v))