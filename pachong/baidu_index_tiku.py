#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-06-22 19:59:25
# Project: baidu_index_tiku

from pyspider.libs.base_handler import *
import MySQLdb
import datetime

conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123",port=3306)
cursor = conn.cursor()

class Handler(BaseHandler):

    crawl_config = {
        'headers': {
            'Cookie': 'PSTM=1464750941; BIDUPSID=E86D6D1C5EB675F2CB9CF17431C6D0F8; BDUSS=1h6VmViVUNZcVdVMUk1fnVCV1IzR1ktVWFCQ0ZFUi1LcENJZWRVeXlHWm52MzFYQVFBQUFBJCQAAAAAAAAAAAEAAACa-JFPsNm80rulwaq4-sut0acAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGcyVldnMlZXa; BDSFRCVID=Er4sJeCCxG3CHUcRDzRi_30n8YUjwFHt67Bc3J; H_BDCLCKID_SF=JbIDVCIytDvWe6rxMtTJ-tCE-fTMetJyaR3Wh45bWJ5TMCoLKbOhy5twQh6NqPviWmnNXnAbafP-ShPC-tPV0PDj3n6r2nbCtaRtKUjy3l02VbLRhhQ2Wf3DMMRfatRMW23r0h7mWU5GVKFCe5-Kjj5QepJf-K6hKCoM0n-8Kb7V-P5mhqn5hnLX-U__5to05TTdQbn7KtoHDR-I5JOVBPu8bMrt26ra-D6X0U7tKRTffjQG5-cr-P4H5MoX-Tra2C6yLnIQ34_MqpcNLUbWQTtdybo2Qf3ELD5doKJ8fUTlj43Dyb8-jUDSDPCE5bj2qRFHoC0M3J; lsv=globalTjs_e63380f-wwwTcss_941ce39-routejs_6ede3cf-activityControllerjs_b6f8c66-wwwBcss_cd6b841-framejs_3109ba6-globalBjs_1d5cdae-sugjs_93b1335-wwwjs_609a8a4; H_WISE_SIDS=104381_103996_107047_100615_100040_106465_102431_107196_100098_107290_107285_106666_104340_107065_107185_103759_103999_106926_106890_104671_107325_107116_107042_104613_104638_107044_107060_107092_106795_100458; MSA_WH=320_568; MSA_PBT=92; MSA_ZOOM=1000; BAIDUID=12455DCFF0A2EEB24A1668FB3AC77E9E:FG=1; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BD_CK_SAM=1; H_PS_PSSID=20145_18286_1453_20318_18280_20368_20388_19690_20417_19861_15142_11478; BD_UPN=123253; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_645EC=e22ao6ItMqNOF%2BuE7PqRhAQIo36xqOHl9e4ph0bKrJAbiYbAH8SYeru51SMIZV6tCJ%2Bk',
        'Host':'www.baidu.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }
    }

    @every(minutes=1 * 3)
    def on_start(self):
        sql = "select url_id from zhanqundb.baidu_recruit_info where spider=0 limit 10000"
        try:
            cursor.execute(sql)
            for (url_id, ) in cursor.fetchall():
                url = 'http://www.genshuixue.com/tiku/%s.html'%(url_id)
                baidu_url = 'https://www.baidu.com/s?wd=' + url + '&rsv_spt=1&rsv_iqid=0xdd34d799000450a7&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=7&rsv_sug1=4&rsv_sug7=100&rsv_sug2=0&inputT=1411&rsv_sug4=1412'
                self.crawl(baidu_url, save={'url': url, 'id': url_id}, callback=self.detail_page)
        except Exception, e:
            print e

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        num = 0
        for each in response.doc('#content_left').items():
            num += 1
        res = response.save
        
        if num > 0:
            sql = "update zhanqundb.baidu_recruit_info set spider=1, recruit=1, recruit_date='%s' where url_id='%s'"%(	datetime.datetime.now().strftime("%Y-%m-%d"), res['id'])
        else:
            sql = "update zhanqundb.baidu_recruit_info set spider=1 where url_id='%s'"%res['id']
        print sql
        
        cursor.execute(sql)
        conn.commit()
        res['num'] = num
        return res
