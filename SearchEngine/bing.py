#! /usr/bin/env python
#-*- coding=utf-8 -*-
import re
import os
import sys
import time
import requests
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
        self.targetUrl = self.readConfig('fishconfig.ini','Bing-Search','SiteUrl')
        self.pageNum = int(self.readConfig('fishconfig.ini','Bing-Search','pageNum'))
        self.keyWord = self.readConfig('fishconfig.ini','Bing-Search','KeyWord')
        self.searchTarget = self.searchUrl.replace('@',self.keyWord)
        self.header = header
        self.header['host'] = 'cn.bing.com'
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

    def dataRequest(self,url):
        '''
        网页获取爬虫
        '''
        print 'dataRequest'
        while True:
            try:
                page = requests.get( url , headers = self.header, timeout = 30 )
            except requests.exceptions.ConnectionError:
                    time.sleep(30)
                    continue
            except requests.exceptions.ConnectTimeout:
                    time.sleep(60)
                    continue
            except requests.exceptions.HTTPError as e:
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
        return html

    def pageGet(self):
        '''
        获取页面
        '''
        print "pageGet"
        urls = []
        title_url = {}
        id_title_url = {}
        for num in range(1,self.pageNum+1):
            urls.append(self.searchTarget.replace('#',str((num-1)*10)))
        for url in urls:
            try:
                page = self.dataRequest(url)
                soup = BeautifulSoup(page)
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
                sites = soup.find_all('h2')
                for site in sites:
                    if site.a:
                        #print site.a.get_text()
                        #print site.a.get('href')
                        #print site.a.get('h')
                        title_url[site.a.get_text()] = site.a.get('href')
                        id_title_url[site.a.get('h')] = title_url.copy()
                        title_url.clear()
        #print title_url
        #print id_title_url
        return  id_title_url

if __name__=="__main__":
    bing = Bing_Search()
    bing.pageGet()
