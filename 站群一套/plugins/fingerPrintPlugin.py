#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-05-10 15:48
 # Filename      : fingerPrintPlugin.py
 # Description   : 计算数据指纹
###########################################################
import sys
import os
import jieba
import jieba.analyse
import logging
from optparse import OptionParser
import urllib,urllib2
from lxml import etree
sys.path.append('../')
import traceback
from iPlugin import Plugin

reload(sys)
sys.setdefaultencoding("utf-8")

__all__ = ["FingerPrintPlugin"]
logger = logging.getLogger('data_compute')

class FingerPrintPlugin(Plugin):
   
    name = "fingerPrintPlugin"
    version = '0.0.1'
    topic_word_num = 1000
    simhash_server_address = 'http://127.0.0.1:11201'
    finger_print_config = {}

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "fingerPrint plugin"

    def processInit(self):
        jieba.load_userdict('conf/jieba_user_dict.txt')
        try:
            for line in open('conf/finger_print.conf'):
                line = line.strip()
                if line.startswith('#'):
                    continue
                else:
                    f = line.split()
                    cls = f[0]
                    subject = f[1]
                    key = '%s_%s'%(cls, subject)
                    self.finger_print_config[key] = 1
        except:
            logger.error('load finger_print.conf exception.')
            return -1
        return 0

    def packetInit(self):
        return 0

    def sendPost(self, data):
        try:
            f = urllib2.urlopen(url=self.simhash_server_address, data=data)
            if f.code == 200:
                return f.read()
            else:
                return None
        except:
            return None

    def run(self, pack):
        data_json = pack['data_json']
        cls = pack['class']
        task_id = pack['task_id']
        id = pack['id']
        subject = data_json['subject']
        data_json['simhash_content'] = '0'
        need_compute = -1
        key = '%s_%s'%(str(cls), subject)
        key = key.encode('utf8')
        if self.finger_print_config.has_key(key):
            need_compute = 1
        #考研资讯
     #   if str(cls) == '46' and subject == u'考研':
     #       need_compute = 1
     #   #雅思资讯
     #   if str(cls) == '17':
     #       need_compute = 1
     #   if str(cls) == '46' and subject == u'雅思':
     #       need_compute = 1
        if need_compute == 1:
            try:
                content = data_json['content']
                tree = etree.HTML(content)
                nodes = tree.xpath("//text()")
                text = ''
                for node in nodes:
                    node = node.strip()
                    text = text + node.replace('\n', '').replace('\t', '')
                tags = jieba.analyse.extract_tags(text, topK=self.topic_word_num)
                tags_str = ",".join(tags).encode('utf8')
                simhash_code = self.sendPost(tags_str)
                if simhash_code == None:
                    simhash_code = '0'
                data_json['simhash_content'] = str(simhash_code)
                pack['data_json'] = data_json
                return 0
            except:
                logger.warn('task_id:%s, id:%s, %s exception.'%(task_id, str(id), self.name))
                pack['data_json'] = data_json
                return 1
        else:
            return 0
