#! /usr/bin/env python
#-*- coding=utf-8 -*-
import re
import os
import sys
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
        self.configFile = './fishconfig.ini'
        self.targetUrl = self.readConfig(self.configFile,'Bing-Search','SiteUrl')
        self.pageNum = int(self.readConfig(self.configFile,'Bing-Search','pageNum'))
        self.Search_KeyWord = self.readConfig(self.configFile,'Bing-Search','Search_KeyWord')
        self.Compare_KeyWord = self.readConfig(self.configFile,'Bing-Search','Compare_KeyWord')
        self.searchTarget = self.searchUrl.replace('@',self.Search_KeyWord)
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
        判断url是https还是http连接
        '''
        print 'sslJudge'
        url = urlparse.urlparse(url_str)
        if url.scheme == 'https':
            return True
        else:
            return False

    def urlCheck(self,url_str):
        '''
        检查url是否完整
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
        获取网页后用BeautifulSoup处理
        返回beautifulsoup格式的对象
        出错返回一个None
        '''
        print 'dataRequest'
        flag = self.sslJudge(url)
        count = 0
        while True:
            try:

                page = requests.get( url , headers = self.header, timeout = 10 , verify = flag )
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
            except requests.exceptions.Timeout:#this is important
                print 'Timeout'
                return None
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
                return None
            else:
                if page.status_code == 200:
                    html = page.content #get page content
                    break
                else:
                    errortext = "Page Code %s " % page.status_code
                    print errortext
                    if count > 1:
                        return None
                    else:
                        count += 1
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
        result = {}
        title_result = []
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
                            title_result.append(site.a.get_text().strip())
                            result[site.a.get('href').strip()] = title_result[:]
                            title_result.pop()
                else:
                    continue
            else:
                continue
        return result

    def titleGet(self,url_title):
        '''
        获取url链接内的网站标题
        返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        '''
        print 'titleGet'
        for url,titles in url_title.iteritems():
            url  = self.urlCheck(url)
            if url:
                page = self.dataRequest(url)
                if page:
                    titles.append(page.title.get_text())
            else:
                continue
        return url_title





    def titleCompare(self,total_titleANDurl):
        '''
        '''
        print 'titleCompare'
        if os.path.exists( './Result/possiblesite_bing.txt' ):
            os.remove('./Result/possiblesite_bing.txt')
        pen = open('./Result/possiblesite_bing.txt','a')
        print total_titleANDurl
        for url,titles in total_titleANDurl.iteritems():
            print 'url',url
            print 'titles[0]',titles[0]
            print 'titles[-1]',titles[-1]
            if self.Compare_KeyWord == titles[0] or self.Compare_KeyWord == titles[-1]:
                pen.write('url:'+url+'\n')
                pen.write('***********'+'\n')
                pen.flush()
            else:
                continue
        pen.close()

if __name__=="__main__":
    bing = Bing_Search()
    #a = bing.dataRequest('http://www.sbacn.org/')
    #print a.title
    urls = bing.pageGet()
    titles=bing.titleGet(urls)
    bing.titleCompare(titles)

    #a= bing.urlCheck('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    #print a
