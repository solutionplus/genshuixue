#ecoding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2,time,socket,json
#socket.setdefaulttimeout(5)
from pyquery import PyQuery as pq
fw = open('/Users/bjhl/Documents/query.done', 'a')
fw1 = open('/Users/bjhl/Documents/seo_res', 'a')
i = 0
for line in open('/Users/bjhl/Documents/900query.txt', 'r'):
    line = line.strip()
    print line
    #line = u'初中'
    for i in range(2,11):
        #加上urllib2.quote(line)!!!
        url = 'http://www.5118.com/seo/words/%s?isPager=true&pageIndex=%s&_=1473823913311' % (urllib2.quote(line), str(i))
        #print '########',url
        request = urllib2.Request(url)
        request.add_header('Cookie',
                           '__cfduid=d0c2292f9ed27f5c3550c60d3e06c24af1473823853; uid=oGflBHmAMcHIZ4tfB%2fxHCm3r9voqr9ZQXggMcFFDUeY%3d; Hm_lvt_295557bac3c4981f18b013f806da26d0=1473823915; Hm_lpvt_295557bac3c4981f18b013f806da26d0=1473823955; Hm_lvt_e51f41cefdaee205c99f313a1a7143f2=1473823946; Hm_lpvt_e51f41cefdaee205c99f313a1a7143f2=1473823955; ASP.NET_SessionId=53g1pwp3so32kera1obrufgj')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        try:
            response = urllib2.urlopen(request)
            while 'captcha' in response.url:
                time.sleep(3000)
                response = urllib2.urlopen(request)
                print response.url
            #解决html转pyquery中文乱码!!!!!!!!!!!!
            data = pq(unicode(response.read(), "utf-8"))
            #print data.html()
            fw.write(line + '\n')
            fw.flush()
            _list = []
            for each in data.find('.dig-list dl:gt(0)').items():
                #print each.html()
                _dict = {}
                _dict['url'] = url
                _dict['query'] = line
                _dict['keyword'] = each.find('.col2-7.word > span > a').text().strip()
                _dict['baidu_ex'] = each.find('dd.center').eq(0).text().strip()
                _dict['search_res'] = each.find('dd.center').eq(1).text().strip()
                _dict['recommend'] = each.find('div > span em').text().strip()
                _list.append(_dict)
            fw1.write(json.dumps(_list)+'\n')
            fw1.flush()
            time.sleep(1)
            #break
        except:
            break
    #break
