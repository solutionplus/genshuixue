#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
dir = '/apps3/rd/yangxiaoyun/zhanqun/online/spider_data/'
filename = sys.argv[1]
fw = open(dir + filename + '.res', 'a')
with open(dir + filename) as f:
    for line in f:
      try:
        #res = line.replace('"', '\\"').replace('${', '$"{').replace('\n','')+'"'+'\n'
        info = json.loads(line.strip().split('$$$$$')[1].replace('\\\\','\\'))
        #if info['date'] == 'null' or not info['date']:
         #   info['date'] = '2016-08-15'
        if len(info['content']) == 0 or len(info['title']) == 0:
            continue
        #info.pop('id')
        #info['class'] = 32
        #info['bread'] = [info['bread'],]
        res = json.dumps(json.dumps(info))+'\n'
        fw.write(line.strip().split('$$$$$')[0]+'$$$$$'+res)
        fw.flush()
      except:
        continue 
fw.close()
