#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-26 14:48
 # Filename      : picFillPlugin.py
 # Description   : 给数据充图，配置文件为conf/pic_fill.conf
###########################################################
import sys
import os
import logging
from lxml import etree
import hashlib
import urllib,urllib2
import redis
import oss2
import re
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["PicFillPlugin"]
logger = logging.getLogger('data_compute')

class PicFillPlugin(Plugin):
   
    name = "picFillPlugin"
    version = '0.0.1'

    HOST = '52a34c024547489a.m.cnbja.kvstore.aliyuncs.com'
    DB = 12
    PORT = 6379
    PASSWD='52a34c024547489a:0s9j09sHSj1sdf1oL'
    ID_GEN = 'zhanqun_id_generator'
    ID_RECORD = 'zhanqun_taskid_record'
    img_url_rec = 'zhanqun_pic_rec'
    client = redis.StrictRedis(host=HOST, port=PORT, db=DB, password=PASSWD)
    auth = oss2.Auth('BPvWuBAlq5rxM3qm', '1EMB2SelO9EQaue3E3xN09zJajB4Dm')
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'genshuixue-public')
    pic_fill_conf = {}
    pic_prefix = "http://img.gsxservice.com/zhanqun/"

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "picFill plugin"

    def processInit(self):
        try:
            for line in open('conf/pic_fill.conf'):
                line = line.strip()
                if line.startswith('#'):
                    continue
                else:
                    f = line.split('\t')
                    cls = f[0]
                    attr = f[1]
                    way = f[2]
                    if self.pic_fill_conf.has_key(cls):
                        self.pic_fill_conf[cls][attr] = way
                    else:
                        self.pic_fill_conf[cls] = {}
                        self.pic_fill_conf[cls][attr] = way
        except:
            logger.error('load pic_fill.conf exception.')
            return -1
        return 0

    def packetInit(self):
        return 0

    def generateFileName(self, imgUrl):
        m2 = hashlib.md5()
        m2.update(imgUrl)
        return m2.hexdigest()

    def uploadImgFile(self, fileName):
        try:
            full_file_name = './data/pics/' + fileName
            with open(full_file_name, 'rb') as fileobj:
                self.bucket.put_object('zhanqun/' + fileName , fileobj)
                return 0
        except:
            return 1

    def getAndSaveImg(self, imgUrl):
        if (len(imgUrl) != 0):
            if self.client.hexists(self.img_url_rec, imgUrl) == 1:
                return self.client.hget(self.img_url_rec, imgUrl)
            imgUrl = imgUrl.strip()
            f = imgUrl.split('.')
            suffix = f[-1]
            if len(suffix) > 5:
                suffix = 'jpg'
            url_md5 = self.generateFileName(imgUrl)
            fileName = url_md5 + '.' + suffix
            try:
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                request = urllib2.Request(imgUrl)
                request.add_header('User-agent', user_agent)
                response = urllib2.urlopen(request)
                ret_code = response.getcode()
                if ret_code != 200:
                    logger.debug('download img with method1 fail:url:%s, new_name:%s' %(imgUrl, fileName))
                    return None
                data = response.read()
                full_file_name = './data/pics/' + fileName
                img_file = file(full_file_name, "wb")
                img_file.write(data)
                img_file.close()
                logger.debug('download img succ:url:%s, new_name:%s' %(imgUrl, fileName))
                flag = self.uploadImgFile(fileName)
                #如果图片上传失败，返回None
                if flag == 1:
                    logger.debug('upload img fail:url:%s, new_name:%s' %(imgUrl, fileName))
                    return None
                else:
                    logger.debug('upload img succ:url:%s, new_name:%s' %(imgUrl, fileName))
                self.client.hset(self.img_url_rec, imgUrl, fileName)
                return fileName
            except:
                logger.warn('getImage or uploadImage exception, url: %s'%(imgUrl))
                return None
        else:
            return None

    def getHost(self, url):
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        return '%s://%s' %(proto,host)

    def run(self, pack):
        task_id = pack['task_id']
        cls = str(pack['class'])
        """ 如果该类没有配置则不需要充图 """
        if cls not in self.pic_fill_conf:
            return 0
        attr_conf = self.pic_fill_conf[cls]
        data_json = pack['data_json']
        subject = data_json['subject']
        must_fill_pic = 0
        #考研的数据必须充图成功，否则丢弃
        if cls == '46' and subject == u'考研':
            must_fill_pic = 1
        if subject == u'动漫' or subject == u'摄影' or subject == u'程序员':
            return 0 
        for key in data_json:
            if attr_conf.has_key(key):
                field = data_json[key]
                way = attr_conf[key]
                try:
                    #1.单值富文本充图
                    if way == '1':
                        tree = etree.HTML(field)
                        nodes=tree.xpath("//img/@src")
                        for node in nodes:
                            if node.startswith('http') or node.startswith('www'):
                                target_url = node
                                if node.startswith('www'):
                                    target_url = '%s%s'%('http://', node)
                            else:
                                #处理相对路径的url
                                target_url = node.strip('../')
                                url = data_json['url']
                                host = self.getHost(url)
                                target_url = '%s/%s'%(host, target_url)
                            new_img_name = self.getAndSaveImg(target_url)
                            if new_img_name == None:
                                if must_fill_pic == 1:
                                    return -1
                                continue
                            else:
                                new_data = self.pic_prefix + new_img_name
                                reg_str = "\"[\S]*%s\"" %(node)
                                reg = re.compile(reg_str)
                                # new_str = '\"%s\"' %(new_data)
                                field = re.sub(reg, '\"%s\"' %(new_data), field)
                        data_json[key] = field
                    #2.多值url充图
                    elif way == '2':
                        new_pic_arr = []
                        for e in field:
                            if e.startswith('http') or e.startswith('www'):
                                target_url = e
                                if e.startswith('www'):
                                    target_url = '%s%s'%('http://', e)
                            else:
                                #处理相对路径的url
                                target_url = e.strip('../')
                                url = pack['url']
                                host = self.getHost(url)
                                target_url = '%s/%s'%(host, target_url)
                            new_img_name = self.getAndSaveImg(target_url)
                            if new_img_name == None:
                                new_pic_arr.append(e)
                            else:
                                new_pic_arr.append(self.pic_prefix + new_img_name)
                        data_json[key] = new_pic_arr
                    #3.单值url充图
                    elif way == '3':
                        e = field
                        if e.startswith('http') or e.startswith('www'):
                            target_url = e
                            if e.startswith('www'):
                                target_url = '%s%s'%('http://', e)
                        else:
                            #处理相对路径的url
                            target_url = e.strip('../')
                            url = pack['url']
                            host = self.getHost(url)
                            target_url = '%s/%s'%(host, target_url)
                        new_img_name = self.getAndSaveImg(target_url)
                        data_json[key] = self.pic_prefix + new_img_name
                    else:
                        continue
                except:
                    logger.warn('task_id:%s, attr:%s, way:%s picFill exception'%(task_id, key, way))
        #将充完图的数据回写到pack包
        pack['data_json'] = data_json
        logger.debug('taskid:%s, pic_fill succ.'%(task_id))
        return 0
