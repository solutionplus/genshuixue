#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-25 15:44
 # Filename      : dataHealthPlugin.py
 # Description   : 对数据进行健康验证，主要验证
 # 1.数据中的schema是否在schema 平台登记；
 # 2.数据的类型是否在schema平台登记；
 # 3.schema中强制要求的schema字段，数据中是否出现并且不为空；
 # 4.schema中单多值验证，数据类型验证
###########################################################
import sys
import os
import sys
import logging
import types
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["DataHealthPlugin"]
logger = logging.getLogger('data_compute')
class DataHealthPlugin(Plugin):
    name = "dataHealthPlugin"
    version = '0.0.1'
    """ class和subject必须声明后才能在数据中使用，否则无法入库 """
    schema_dict = {}
    subject_dict = {}


    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "dataHealth plugin"

    def processInit(self):
        try:
            """ 加载属性词典,db:schema_attr_test """
            file = open('conf/schema.dict')
            schema = file.read()
            file.close()
            schema_dict_tmp = eval(schema)
            for id in schema_dict_tmp.keys():
                data_type_dict = {}
                is_must_dict = {}
                is_mul_dict = {}
                name_dict = {}
                attr_arr = schema_dict_tmp[id]
                for tmp in attr_arr:
                    name = tmp['name']
                    name_dict[name] = 1
                    data_type_dict[name] = tmp['data_type']
                    is_must_dict[name] = tmp['is_must']
                    is_mul_dict[name] = tmp['is_mul']
                self.schema_dict[id] = {}
                self.schema_dict[id]['data_type_dict'] = data_type_dict
                self.schema_dict[id]['is_must_dict'] = is_must_dict
                self.schema_dict[id]['is_mul_dict'] = is_mul_dict
                self.schema_dict[id]['name_dict'] = name_dict

            """ 加载subject词典,db:subject """
            for line in open('conf/subject.conf'):
                line = line.strip()
                line = line.decode('utf8')
                if self.subject_dict.has_key(line):
                    pass
                else:
                    self.subject_dict[line] = 1
            return 0
        except:
                logger.error('processInit exception.')
                return -1

    def packetInit(self):
        return 0

    def run(self, pack):
        task_id = pack['task_id']
        if 'data_json' not in pack:
            logger.warn('data_json is not in pack.')
            return -1
        data_json = pack['data_json']

        """
            step1. class和subject验证，如果该数据对应的class在schema平台中没有设置，则返回-1,该数据无效
        """
        if 'subject' not in data_json or 'class' not in data_json:
            logger.error('task_id:%s has no subject or class, please check.'%(task_id))
            return -1
        cls = str(data_json['class'])
        if cls not in self.schema_dict:
            logger.error('task_id:%s, cls:%s is not exist, please check data_resove_config table.'%(task_id, cls))
            return -1
        subject = data_json['subject']
        if subject not in self.subject_dict:
            logger.error('task_id:%s, subject:%s is not exist, please check.'%(task_id, subject))
            return -1
        """ 
            step2. 属性名验证，如果数据中的属性名在schema平台中没有设置，则返回-1
        """
        info_dict = self.schema_dict.get(cls)
        for key in data_json:
            if info_dict['name_dict'].has_key(key):
                continue
       #     elif key == 'class':
        #        continue
            else:
                logger.warn('task_id:%s, cls:%s, attr:\"%s\" is not exist in database.'%(task_id, cls, key))
                return -1

        """
            step3. is_must验证,验证必须字段是否存在(存在不能为空)，不存在返回1,丢弃该数据
        """
        for key in info_dict['is_must_dict']:
            if info_dict['is_must_dict'][key] == 1:
                if key not in data_json:
                    logger.warn('task_id:%s, attr: %s is must, but not exist in data'%(task_id, key))
                    return -1
                if data_json[key] == None:
                    logger.warn('task_id:%s, attr: %s is must, but is None'%(task_id, key))
                    return -1
                if data_json[key] == "":
                    logger.warn('task_id:%s, attr: %s is must, but is empty string'%(task_id, key))
                    return -1
        """
            step4. is_mul和data_type验证
        """
        #print data_json.keys()
        for key in data_json:
            """ list """
            # print type(data_json[key])
            # print info_dict['data_type_dict'][key]
            if info_dict['is_mul_dict'][key] == 1:
                if type(data_json[key]) is types.NoneType:
                    continue
                """ 如果是多值,则判断值的类型"""
                if type(data_json[key]) is types.ListType:
                    if len(data_json[key]) == 0:
                        continue
                    else:
                        v = data_json[key][0]
                        """ 字符串类型 or json类型 """
                        if info_dict['data_type_dict'][key] == 1:
                            if type(v) is types.StringType or type(v) is types.UnicodeType:
                                continue
                            else:
                                logger.warn('task_id:%s, attr:%s is_mul, str validate fail.'%(task_id, key))
                                return -1
                        elif info_dict['data_type_dict'][key] == 2:
                            if type(v) is types.DictType:
                                continue
                            else:
                                logger.warn('task_id:%s, attr:%s is_mul, json validate fail.'%(task_id, key))
                                return -1
                        elif info_dict['data_type_dict'][key] == 3:
                            if type(v) is types.IntType or type(v) is types.FloatType:
                                continue
                            else:
                                logger.warn('task_id:%s, attr:%s is_mul,numerical validate fail.'%(task_id, key))
                                return -1
                        else:
                            logger.warn('task_id:%s, attr:%s is_mul,value type validate fail.'%(task_id, key))
                            return -1
                else:
                    logger.warn('task_id:%s, attr:%s is_mul validate fail.'%(task_id, key))
                    return -1
            else:
                if type(data_json[key]) is types.NoneType:
                    continue
                """ 字符串 or json类型 """
                if info_dict['data_type_dict'][key] == 1:
                    if type(data_json[key]) is types.StringType or type(data_json[key]) is types.UnicodeType:
                        continue
                    else:
                        logger.warn('task_id:%s, attr:%s is_mul validate fail.'%(task_id, key))
                        return -1
                elif info_dict['data_type_dict'][key] == 2:
                    if type(data_json[key]) is types.DictType:
                        continue
                    else:
                        logger.warn('task_id:%s, attr:%s is_mul validate fail.'%(task_id, key))
                        return -1
                elif info_dict['data_type_dict'][key] == 3:
                    v = data_json[key]
                    if type(v) is types.IntType or type(v) is types.FloatType:
                        continue
                    else:
                        logger.warn('task_id:%s, attr:%s is_mul,numerical validate fail.'%(task_id, key))
                        return -1
                elif info_dict['data_type_dict'][key] == 4:
                    v = data_json[key]
                    if type(v) is types.IntType or type(v) is types.FloatType:
                        continue
                    else:
                        logger.warn('task_id:%s, attr:%s is_mul,numerical validate fail.'%(task_id, key))
                        return -1
                else:
                    logger.warn('task_id:%s, attr:%s is_mul validate fail.'%(task_id, key))
                    return -1
        #logger.info('task_id:%s data_healty succ.'%(task_id))
        return 0
