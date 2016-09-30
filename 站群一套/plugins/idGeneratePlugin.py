#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-25 20:51
 # Filename      : idGeneratePlugin.py
 # Description   : 给数据自动生成id
 # output:id, redis_id, update_time, source 
###########################################################
import sys
import os
import logging
import redis
import time
import json
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["IdGeneratePlugin"]
logger = logging.getLogger('data_compute')
class IdGeneratePlugin(Plugin):
   
    name = "idGeneratePlugin"
    version = '0.0.1'
    HOST = '52a34c024547489a.m.cnbja.kvstore.aliyuncs.com'
    DB = 12
    PORT = 6379
    PASSWD='52a34c024547489a:0s9j09sHSj1sdf1oL'
    ID_GEN = 'zhanqun_id_generator'
    ID_RECORD = 'zhanqun_taskid_record'
    client = redis.StrictRedis(host=HOST, port=PORT, db=DB, password=PASSWD)

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "idGenerate plugin"

    def processInit(self):
        return 0

    def packetInit(self):
        return 0

    def get_id(self, task_id):
        if self.client.hexists(self.ID_RECORD, task_id):
            id = self.client.hget(self.ID_RECORD, task_id)
            return id
        else:
            id = self.client.incr(self.ID_GEN)
            self.client.hset(self.ID_RECORD, task_id, id)
            return id

    def run(self, pack):
        try:
            task_id = pack['task_id']
            data_json = pack['data_json']
            cls = data_json['class']
            redis_id = '%s_%s'%(task_id, cls)
            id = self.get_id(redis_id)
            task_id = '%s_%s'%(task_id, cls)
            source = data_json['source']
            ISOTIMEFORMAT='%Y-%m-%d %X'
            update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
            pack['id'] = id
            pack['class'] = cls
            pack['source'] = source
            pack['update_time'] = update_time
            pack['redis_id'] = task_id
            #record = '%s%s%s%s%s%s' %(id, cls, json.dumps(data_json), source, update_time, task_id)
            # pack['record'] = record
        except:
            logger.error('taskid:%s run fail.'%(task_id))
            return -1
        return 0
