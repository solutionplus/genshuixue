# -*- encoding: utf-8 -*-
# Created on 2016-07-04 15:44:10
# Project: keyword_monitor_m

from pyspider.libs.base_handler import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urlparse
import time
import json

def qs(url):
    query = urlparse.urlparse(url).query
    return dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])

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

    index_dict = {}
    
    @every(minutes=3 * 24 * 60)
    def on_start(self):
        with open('/apps/home/rd/hexing/data/keyword','r') as f:
            for line in f:
                if line :
                    line = line.strip()
                    arr = line.split('\t')
                    for index in range(10):
                        self.crawl('https://www.baidu.com/s?wd=%s&pn=%s&rsv_spt=1&rsv_iqid=0xa0eaa7930001b982&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=1&rsv_sug2=0&inputT=995&rsv_sug4=995'%(arr[0],index*10),save = {'query':arr[0],'info':json.loads(arr[1])},priority = 100 - index * 10,callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
      if response.save.get('query') not in self.index_dict:
            time.sleep(1)
            for index , each in enumerate(response.doc('.result').items()):
                _dict = {}
                _dict['title'] = each.find('h3 a').text()
                _dict['query'] = response.save.get('query')
                _dict['url'] = each.find('.f13 a').text()
                _dict['info'] = response.save.get('info')
                #url =  each.find('h3 a').attr.href
                page_dict = qs(response.url)
                if 'pn' not in page_dict:
                    pn = 0
                else:
                    pn = page_dict['pn']
                if 'genshuixue' in _dict['url']:
                    self.index_dict[response.save.get('query')] = index + 1 + int(pn)      
                    _dict['rank'] = index + 1 +int(pn)
                    return _dict
                    #self.crawl(url, save =_dict,callback=self.detail_page)
       

    @config(priority=2)
    def detail_page(self, response):
        #res_dict = response.save
        #res_dict['index'] = self.index_dict[response.save.get('query')]
        #return res_dict
        pass