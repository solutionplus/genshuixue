#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys,urllib2,os
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib

for line in open('/tmp/20160901191549f4cf/haoshengyin.query','r'):

    m2 = hashlib.md5()
    m2.update(line.strip())
    m = m2.hexdigest()
    #url = 'http://www.genshuixue.com/i-changge/x/'+m+'.html'
    url = 'http://172.16.1.45:9200/corpora_index_v2_b/normal/%s'%m
    print url
    try:
        os.system('curl -XDELETE %s' % url)
        #break
    except Exception as ee:
        print  ee.message
        continue
