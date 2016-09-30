#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-26 16:48
 # Filename      : summaryPlugin.py
 # Description   : 
###########################################################
import sys
import os
import json
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["SummaryPlugin"]

class SummaryPlugin(Plugin):
   
    name = "summaryPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "summary plugin"

    def processInit(self):
        return 0

    def packetInit(self):
        return 0

    def run(self, pack):
        try:
            id = pack['id']
            cls = pack['class']
            content = json.dumps(pack['data_json'])
            source = pack['source']
            update_time = pack['update_time']
            redis_id = pack['redis_id']
            result = '%s%s%s%s%s%s'%(id, cls, content, source, update_time, redis_id)
            pack['result'] = result
        except:
            logger.error('SummaryPlugin run fail.')
            return -1
        return 0
