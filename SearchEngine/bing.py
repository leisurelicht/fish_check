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
        'Accept-Encoding' : 'gzip, deflate','DNT' : '1',
        'Connection' : 'keep-alive'
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
        url = urlparse.urlparse(url_str)
        print url
        if url.netloc == '':
            return None
        elif url.scheme == '':
            url.scheme == 'http'
        #return urlparse.urlunsplit(url) 
    def dataRequest(self,url):
        '''
        网页获取爬虫
        '''
        print 'dataRequest'
        print url
        flag = self.sslJudge(url)
        print flag
        while True:
            try:

                page = requests.get( url , headers = self.header, timeout = 30 , verify = flag)
            except requests.exceptions.ConnectionError:
                print 'ConnectionError'
                time.sleep(30)
                continue
            except requests.exceptions.ConnectTimeout:
                print 'ConnectTimeout'
                time.sleep(60)
                continue
            except requests.exceptions.SSLError:
                print 'SSLError'
                flag = False
                #continue
            except requests.exceptions.HTTPError as e:
                print 'HTTPError'
                time.sleep(600)
                continue
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
            return NULL
        else:
            return soup

    def pageGet(self):
        '''
        获取页面
        '''
        print "pageGet"
        urls = []
        urls_2 = []
        for num in range(1,self.pageNum+1):
            urls.append(self.searchTarget.replace('#',str((num-1)*10)))
        for url in urls:
            print url
            try:
                page = self.dataRequest(url)
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
            else:
                sites = page.find_all('h2')
                for site in sites:
                    if site.a:
                        #print site.a.get('href')
                        urls_2.append(site.a.get('href'))
        return urls_2

    def titleGet(self,urls):
        '''
        '''
        print 'titleGet'
        for url in urls:
            self.dataRequest(url)




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
    #urls = bing.pageGet()
    #bing.titleGet(urls)
    a  = bing.urlCheck('cn.bing.com/entities/search?q=%e4%b8%8a%e6%b5%b7%e9%93%b6%e8%a1%8c&filters=segment%3a%22local%22&pin=YN4067x7364153967624808703%2cYN4067x14496301%2cYN4067x16635168860261914832%2cYN4067x2545510891879138457%2cYN4067x23442530&FORM=LARE')
    #a= bing.urlCheck('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    print a 
