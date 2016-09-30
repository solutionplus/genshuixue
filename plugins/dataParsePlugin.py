#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-25 15:37
 # Filename      : dataParsePlugin.py
 # Description   : 将数据进行解析,字符串解析为json串,
 # output: data_json, class, subject, task_id
###########################################################
import sys
import os
import sys
import json
import logging
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["DataParsePlugin"]

logger = logging.getLogger('data_compute')
class DataParsePlugin(Plugin):
   
    name = "dataParsePlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def processInit(self):
       return 0 

    def packetInit(self):
        return 0

    def scan(self, config={}):
        return "dataParsePlugin"
    
    def run(self, pack):
        if 'origin_data' not in pack:
            logger.warn('origin_data is not in pack, please check, pack:%s'%(pack))
            return -1
        else:
            try:
                data_str = pack['origin_data']
                data_str = data_str.strip()
                delem = '$$$$$'
                f = data_str.split(delem)
                task_id = f[0]
                pack['task_id'] = f[0]
                #print f[1]
                content_str = json.loads(f[1])
               # print content_str
                data_json = json.loads(content_str)
                if 'data_weight' not in data_json:
                    data_json['data_weight'] = 0
                #test
              #  data_json['class'] = 46
              #  data_json['subject'] = u'作文'
              #  data_json['source'] = 'test'
              #  data_json['data_weight'] = 0

              #  print data_json.keys()
                if 'source' not in data_json or 'subject' not in data_json or 'class' not in data_json:
                    logger.error('task_id:%s must has attr source subject and class, please check.'%(task_id))
                    return -1
                pack['data_json'] = data_json
                pack['class'] = data_json['class']
                pack['subject'] = data_json['subject']
                #logger.info('%s:%s run succ'%(self.name, task_id))
            except Exception as e:
                logger.warn('%s parse exception, %s'%(self.name, e))
                return -1
            return 0 
