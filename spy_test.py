# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

class Spider:

# ToDO:
# - Timeout setting

    def __init__(self):
        #self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.siteURL = 'http://www.1point3acres.com/bbs/forum-28-1.html'
        # self.siteURL = 'http://www.mitbbs.com/bbsdoc/JobHunting.html'
    def getPage(self,pageIndex):
        self.setProxy()
        url = self.siteURL + "?page=" + str(pageIndex)
        print "======================================="
        print "reading url: ", url
        print "======================================="
        request_headers = {
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "http://www.1point3acres.com/bbs/",
        "Connection": "keep-alive"
        }
        try:
            request = urllib2.Request(url, headers = request_headers)
            response = unicode(urllib2.urlopen(request).read(),'GBK').encode('UTF-8')
            # print "================response==============="
            # print  response
            return response
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
    def setProxy(self):
        enable_proxy = True
        proxy = "http://www.baidu.com:8080"
        proxy_handler = urllib2.ProxyHandler({"https" : proxy})
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)
        print "proxy has been set to ",proxy

    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        parse1 = '<tbody.*?tdpre y".*?void\(0\)\;(.*?)"previewThread.*?<em>.*?<a.*?>(.*?)</a>.*?</em>.*?<td.*?num.*?<a href="(.*?)".*?class'
        pattern = re.compile(parse1,re.S)
        items = re.findall(pattern,page)
        print "=================Items1================="
        for item in items:
             print item[0].strip() + " " + item[2].strip() + " " + item[1].strip()
        print "=================Items1 End================="
        parse2 = '<tbody.*?<em>.*?">(.*?)</a>.*?<a.*?"(.*?)".*?xst">(.*?)</a>'
        pattern = re.compile(parse2,re.S)
        items2 = re.findall(pattern,page)
        print "=================Items2================="
        for item in items2:
             print item[0].strip() + " " + item[2].strip() + " " + item[1].strip()
        print "=================Items2 End================="
        print "======================================="
        print "Done! Page loaded!"

spider = Spider()
spider.getContents(1)
