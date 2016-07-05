# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

class YMSFDClawer:
    """A clawer for 1 point 3 arcs websites, aiming to find the related information for specific company"""
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        #initialize headers
        self.headers = {
                "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": "http://www.1point3acres.com/bbs/",
                "Connection": "keep-alive"
                 }
        # The loadedPages list for every page
        self.loadedPages = []
        #determint if the program keep running
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.1point3acres.com/bbs/forum-28-1.html' + '?page=' + str(pageIndex)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = unicode(response.read(),'GBK').encode('UTF-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "failed to connect website, reason: ",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "failed to load page...."
            return None
        pattern = re.compile('<tbody.*?<em>.*?">(.*?)</a>.*?<a.*?"(.*?)".*?xst">(.*?)</a>',re.S)
        items = re.findall(pattern,pageCode)
        postsOfPage = []
        for item in items:
            if item[0].strip()=="找工就业":
                postsOfPage.append([item[2].strip(), item[1].strip()])
        print "Fetched " + str(len(postsOfPage)) + " related loadedPages on page " + str(pageIndex) + "..."
        return postsOfPage

    def loadPage(self):
        if self.enable == True:
            if len(self.loadedPages) < 2:
                postsOfPage = self.getPageItems(self.pageIndex)
                if postsOfPage:
                    self.loadedPages.append(postsOfPage)
                    self.pageIndex += 1

    def getPostsFromOnePage(self,postsOfPage,page):
        input = raw_input()
        if input == "Q":
            self.enable = False
            return
        for post in postsOfPage:
            print "Page %d\t Title:%s\t Url:%s" %(page, post[0], post[1])
        self.loadPage()

    def start(self):
        print u"Reading from 1 point 3 archs website，press Q to exit"
        self.enable = True
        # load first page
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.loadedPages)>0:
                postsOfPage = self.loadedPages[0]
                nowPage += 1
                # delete the posts extracted
                del self.loadedPages[0]
                # print posts from page
                self.getPostsFromOnePage(postsOfPage,nowPage)


spider = YMSFDClawer()
spider.start()
