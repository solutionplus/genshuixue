#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-04 18:18:03
# Project: yitongdai

import re
import time
from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb3 import SQL


class Handler(BaseHandler):
    
    headers= {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
    }
    cookies = {
  "ATA1253407868": "1907389353-1467635488-%7C1468296757", 
  "Hm_lpvt_6abc8f820c003b71587d5619f3080cc1": "1468299416", 
  "Hm_lvt_6abc8f820c003b71587d5619f3080cc1": "1.46763937314677E+29", 
  "JSESSIONID": "4311B024BF094E87F2C00E5EEEE5F7DB", 
  "_adwb": "203813312", 
  "_adwc": "203813312", 
  "_adwp": "203813312.8507941580.1467639373.1468228418.1468299415.10", 
  "_adwr": "203813312%230", 
  "_aitcmurl": "http%3A//app.etongdai.com/firend/myfirends%3FpageId%3D1%26friendType%3D0", 
  "_jstar": "%26ct%3D1468228419133", 
  "_jzqa": "1.871219523436518700.1467639374.1468228419.1468299416.10", 
  "_jzqb": "1.1.10.1468299416.1", 
  "_jzqc": "1", 
  "_jzqckmp": "1", 
  "_jzqx": "1.1467703973.1468299416.4.jzqsr=app%2Eetongdai%2Ecom|jzqct=/account/index.jzqsr=app%2Eetongdai%2Ecom|jzqct=/firend/myfirends", 
  "_qzja": "1.1739382353.1467639374263.1468228418974.1468299415883.1468228418974.1468299415883.0.0.0.56.10", 
  "_qzjb": "1.1468299415882.1.0.0.0", 
  "_qzjc": "1", 
  "_qzjto": "1.1.0", 
  "_userId": "4237738", 
  "_username": "qjcm", 
  "tq_current_source_page_url": "https://app.etongdai.com/login/index", 
  "tq_current_visit_time": "1468215434305", 
  "tq_source_page_url": "https://app.etongdai.com/login/index", 
  "username": "qjcm"




    }
    crawl_config = {
        "headers" : headers,
        "cookies" : cookies,
        "itag" : 'v02',
       # "method" : 'POST',
     
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://app.etongdai.com/firend/myfirends?friendType=0',age=20*60,auto_recrawl=True,force_update=True,callback=self.detail_page)
        self.crawl('http://app.etongdai.com/firend/myfirends?friendType=0',callback=self.index_page)
        #self.crawl('http://www.moguozi.com/index.php/admin/admin/login.html')      
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.btn').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert = False)

          
      
    @config(priority=2)
    def detail_page(self, response):
        for each in response.doc('.btn').items():
             self.crawl(each.attr.href,priority=9,callback=self.detail_page, validate_cert = False)
        
        for i, each in enumerate(response.doc('.from tr:not(:first-child)').items()):
            self.send_message(self.project_name, {
                "uer_id": each('th').eq(0).text(),
                'user_date': each('th').eq(1).text(),
                'content': each('th').eq(2).text(),
                'type': each('th').eq(3).text(),
                'operate': each('th').eq(4).text(),
            }, url="%s#%s" % (response.url,i))

    def on_message(self, project, msg):
        return msg
    
    def on_result(self, result):
        if not result or not result['uer_id']:
            return
        super(Handler, self).on_result(result)
        sql = SQL()
        sql.replace('yitongdai',**result)    
 
      
        

          
    
    
    
    
    
    
    
    