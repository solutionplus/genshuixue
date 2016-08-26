#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-22 19:28:01
# Project: wenda_baidu
from pyspider.libs.base_handler import *
import MySQLdb
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "123", db = "querydb", charset = "utf8")
cursor = conn.cursor()

class Handler(BaseHandler):
    crawl_config = {
        "itag":'0.1',
        "headers": {
        'Host': 'www.baidu.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
    }
    

    @every(minutes=1 * 30)
    def on_start(self):
        sql = 'select id, query from tb_query where flag = 0 limit 100'
        try:
            cursor.execute(sql)
            for (query_id, query,) in cursor.fetchall():
                #query = unicode(query, 'utf-8')
                #print query
                #word = 'good'
                for i in range(0,60,10):
                    self.crawl('http://zhidao.baidu.com/search?lm=0&rn=10&pn=%s&fr=search&ie=utf8&word=%s'%(str(i),query),save = {'query':query, 'id':query_id},callback=self.index_page)
        except Exception,e:
            print e
            

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.dl').items():
            _dict = {}
            _dict['id'] = response.save.get('id') 
            _dict['query'] = response.save.get('query') 
            _dict['title'] = each.find('.line > a').text()
            url = each.find('.line > a').attr.href
            _dict['create_time'] = each.find('.mr-8').text().split()[0]
            self.crawl(url, save = _dict,callback=self.detail_page)
        for each in response.doc('.mb-20 > dl').items():
            _dict = {}
            _dict['id'] = response.save.get('id') 
            _dict['query'] = response.save.get('query') 
            _dict['title'] = each.find('.mb-8 > a').text()
            url = each.find('.mb-8 > a').attr.href
            _dict['create_time'] = each.find('.mr-8').text().split()[0]
            self.crawl(url, save = _dict,callback=self.detail_page)
        #翻页
        #for each in response.doc('.pager-next').items():
         #   self.crawl(each.attr.href, save = response.save, callback=self.index_page)   
       

    @config(priority=2)
    def detail_page(self, response):
        query_id = response.save.get('id')
        sql = "update tb_query set flag=1 where id=%s" % (query_id)
        try:           
            cursor.execute(sql)
            conn.commit()
        except Exception, e:
            print e
        #if response.doc('.word-replace'):
        #    return
        res_dict = response.save
        res_dict['url'] = response.url
        res_dict['source'] = 'baidu'
        res_dict['subject'] = u'主站问答'
        res_dict['category_id'] = []
        res_dict['class'] = 34
        #print response.doc('.q-content').html()
        res_dict['question_detail'] = response.doc('.q-content').text() if not response.doc('.q-content .word-replace') else ''
        
        answers_list = []
        if response.doc('.content > .mb-10'):
            if not response.doc('.content > .mb-10 .word-replace'):
                if response.doc('.question-list-item-tag > a'):
                    res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
                if  response.doc('div.mb-15 > .pos-time'):
                    create_time = response.doc('div.mb-15 > .pos-time').text().split()[0]
                else:
                    create_time = time.strftime('%Y-%m-%d',time.localtime())
                answers_list.append({
                    "content":  response.doc('.content > .mb-10').html().strip(),
                    "create_time": create_time,
                    "user_name": response.doc('div.mt-10').text(),
                })
        if response.doc('.quality-content > .quality-content-detail'):
            if not response.doc('.quality-content > .quality-content-detail .word-replace'):
                if response.doc('.question-list-item-tag > a'):
                    res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
                if response.doc('.quality-info > .reply-time'):
                    create_time = response.doc('.quality-info > .reply-time').text().split()[0]
                else:
                    create_time = time.strftime('%Y-%m-%d',time.localtime())
                answers_list.append({
                    "content":  response.doc('.quality-content > .quality-content-detail').html().strip(),
                    "create_time": create_time,
                    "user_name": response.doc('.q-name > a').text(),
                })
        if response.doc('.ec-answer'):
            #print u'企业回答'
            if not response.doc('.ec-answer .word-replace'):
                if response.doc('.question-list-item-tag > a'):
                    res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
                if  response.doc('.ec-time'):
                    create_time = response.doc('.ec-time').text().split()[0]
                else:
                    create_time = time.strftime('%Y-%m-%d',time.localtime())
                answers_list.append({
                    "content":  response.doc('.ec-answer').html().strip(),
                    "create_time": create_time,
                    "user_name": '',
                })
        if response.doc('.best-related dd > span'):
            if not response.doc('.best-related dd > span .word-replace'):
                if response.doc('.question-list-item-tag > a'):
                    res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
                res_dict['question_detail'] = response.doc('.qb-content').html()
                if  response.doc('.best-related i > span'):
                    create_time = response.doc('.best-related i').eq(-1).text().split()[0]
                    user_name = response.doc('.best-related i').eq(0).text()
                else:
                    create_time = time.strftime('%Y-%m-%d',time.localtime())
                    user_name = ''
                answers_list.append({
                    "content":  response.doc('.best-related dd > span').html().strip(),
                    "create_time": create_time,
                    "user_name": user_name,
                })
        for each in response.doc('div.answer-text').items():
            if each.find('.word-replace'):
                continue
            if response.doc('.question-list-item-tag > a'):
                res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
            if  each.parent().prev().find('.pos-time'):
                create_time = each.parent().prev().find('.pos-time').text().split()[0]
                if not each.parent().prev().find('.pos-time').next():
                    user_name = each.parent().prev().remove('.pos-time').text()
                else:
                    user_name = each.parent().prev().find('.pos-time').next().text()
            else:
                create_time = time.strftime('%Y-%m-%d',time.localtime())
                user_name = ''
            answers_list.append({
                "content":  each.html().strip(),
                "create_time": create_time,
                "user_name": user_name,
            })
        for each in response.doc('dl.other-answer > .answer').items():
            if each.find('.word-replace'):
                continue
            if response.doc('.question-list-item-tag > a'):
                res_dict['category_id'] = [v.text() for v in response.doc('.question-list-item-tag > a').items() if v]
            res_dict['question_detail'] = response.doc('.qb-content').html()
            if  each.find('.ext-info > i'):
                create_time = each.find('.ext-info > i').eq(-1).text()
            else:
                create_time = time.strftime('%Y-%m-%d',time.localtime())
            answers_list.append({
                "content":  each.children().eq(0).html().strip(),
                "create_time": create_time,
                "user_name": each.find('.ext-info > i').eq(0).text(),
            })
        if len(answers_list) == 0:
            return
        res_dict['answers'] = answers_list
        res_dict['data_weight'] = 0
        res_dict['create_user'] = response.doc('.ask-info > span').eq(1).text()
        return res_dict
