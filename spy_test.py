# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

class Spider:

    def __init__(self):
        #self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        #self.siteURL = 'http://www.1point3acres.com/bbs/forum-28-1.html'
        self.siteURL = 'http://www.mitbbs.com/bbsdoc/JobHunting.html'
    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print url
        # headers = headers={"Accept" : "text/html"}
        request_headers = {
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "http://www.mitbbs.com/bbsboa/1.html",
        "Connection": "keep-alive"
        }
        request = urllib2.Request(url, headers = request_headers)
        response = urllib2.urlopen(request)
        print "response"
        print response.read()
        return response.read().decode('gbk')

    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            print item[0],item[1],item[2],item[3],item[4]

spider = Spider()
spider.getContents(1)
