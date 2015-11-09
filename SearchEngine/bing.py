#! /usr/bin/env python
#-*- coding=utf-8 -*-
import re
import os
import sys
import time
import requests
import urlparse
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding('utf8')

header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding' : 'gzip, deflate',
        }

class Bing_Search(object):
    """docstring for Bing_Search"""
    def __init__(self,):
        super(Bing_Search, self).__init__()
        self.searchUrl = 'http://cn.bing.com/search?q=@&go=提交&first=#'
        self.configFile = '../fishconfig.ini'
        self.targetUrl = self.readConfig(self.configFile,'Bing-Search','SiteUrl')
        self.pageNum = int(self.readConfig(self.configFile,'Bing-Search','pageNum'))
        self.keyWord = self.readConfig(self.configFile,'Bing-Search','KeyWord')
        self.searchTarget = self.searchUrl.replace('@',self.keyWord)
        self.header = header
        #self.header['host'] = 'cn.bing.com'
        self.header['Referer'] = 'http://cn.bing.com/'


    def readConfig(self,iniFile,section,option):
        '''
        读取配置文件
        '''
        print 'readConfig'
        try:
            config = ConfigParser()
            config.read(iniFile)
        except Exception:
            print "无法读取配置文件"
        else:
            return config.get(section,option)

    def sslJudge(self,url_str):
        '''
        '''
        print 'sslJudge'
        url = urlparse.urlparse(url_str)
        if url.scheme == 'https':
            return True
        else:
            return False

    def urlCheck(self,url_str):
        '''
        '''
        print 'urlCheck'
        url = urlparse.urlsplit(url_str)
        if url.netloc == '':
            return None
        else:
            if url.scheme == '':
                url.scheme == 'http'
                return urlparse.urlunsplit(url)
            else:
                return url_str

    def dataRequest(self,url):
        '''
        网页获取爬虫
        '''
        print 'dataRequest'
        flag = self.sslJudge(url)
        print flag
        count = 0
        while True:
            try:

                page = requests.get( url , headers = self.header, timeout = 10 , verify = flag )
                print page.url
            except requests.exceptions.ConnectionError:
                print 'ConnectionError'
                if flag == True:
                    flag = False
                    count += 1
                    continue
                if count > 1:
                    return None
                else:
                    count += 1
                    continue
            except requests.exceptions.ConnectTimeout:
                print 'ConnectTimeout'
                if count > 1:
                    return None
                else:
                    count += 1
                    continue
            except requests.exceptions.ReadTimeout:
                print 'ReadTimeout'
                if count > 1:
                    return None
                else:
                    count += 1
                    continue
            except requests.exceptions.TooManyRedirects:
                print 'TooManyRedirects'
                return None
            except requests.exceptions.SSLError:
                print 'SSLError'
                flag = False
                continue
            except requests.exceptions.HTTPError:
                print 'HTTPError'
                return None
            except requests.exceptions.RequestException as e:
                errortext = "Error in function : \" %s \" ,\n \
                    Error name is : \" %s \" ,\n \
                    Error type is : \" %s \" ,\n \
                    Error Message is : \" %s \" ,\n \
                    Error doc is : \" %s \" \n" % \
                (sys._getframe().f_code.co_name,\
                     e.__class__.__name__,\
                     e.__class__,\
                     e,\
                     e.__class__.__doc__)
                print errortext
                continue
            else:
                if page.status_code == 200:
                    html = page.content #get page content
                    break
                else:
                    errortext = "Page Code %s " % page.status_code
                    print errortext
                    continue
        try:
            soup = BeautifulSoup(html)
        except Exception as e:
            errortext = "Error in function : \" %s \" ,\n \
                    Error name is : \" %s \" ,\n \
                    Error type is : \" %s \" ,\n \
                    Error Message is : \" %s \" ,\n \
                    Error doc is : \" %s \" \n" % \
                    (sys._getframe().f_code.co_name,\
                     e.__class__.__name__,\
                     e.__class__,\
                     e,\
                     e.__class__.__doc__)
            print errortext
            return None
        else:
            return soup

    def pageGet(self):
        '''
        获取页面
        '''
        print "pageGet"
        urls_search = []
        urls_result = []
        for num in range(1,self.pageNum+1):
            urls_search.append(self.searchTarget.replace('#',str((num-1)*10)))
        for url in urls_search:
            url  = self.urlCheck(url)
            if url:
                page = self.dataRequest(url)
                if page:
                    sites = page.find_all('h2')
                    for site in sites:
                        if site.a:
                            #print site.a.get('href')
                            urls_result.append(site.a.get('href').strip())
                else:
                    continue
            else:
                continue
        return urls_result

    def titleGet(self,urls):
        '''
        '''
        print 'titleGet'
        for url in urls:
            print url
            url  = self.urlCheck(url)
            if url:
                page = self.dataRequest(url)
                if page:
                    print page.title

            else:
                continue




    def titleCompare(self,total_titleANDurl):
        '''
        '''
        print 'titleCompare'
        if os.path.exists( '../possiblesite_bing.txt' ):
            os.remove('../possiblesite_bing.txt')
        pen = open('../possiblesite_bing.txt','a')
        for titleANDurl in total_titleANDurl:
            for title,url in titleANDurl.iteritems():
                print title
                if title == self.keyWord:
                    pen.write('title:'+title+'\n')
                    pen.write('url:'+url+'\n')
                    pen.write('***********'+'\n')
                    pen.flush()
                    #if self.pageCompare(self.targetUrl,url):
                    #    print '开始记录可能的钓鱼网站'
                    #    pen.write('title:'+title)
                    #    pen.write('url:'+url)
                    #    pen.write('***********')
                    #    pen.flush()
                    #else:
                    #    print '检查下一个网站'
                else:
                    continue
        pen.close()

if __name__=="__main__":
    bing = Bing_Search()
    #a = bing.dataRequest('http://www.sbacn.org/')
    #print a.title
    urls = bing.pageGet()
    bing.titleGet(urls)
    #a= bing.urlCheck('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    #print a
