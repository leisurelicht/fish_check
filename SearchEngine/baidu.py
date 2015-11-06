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

class Baidu_Search(object):
    """docstring for Baidu_Search"""
    def __init__(self,):
        super(Baidu_Search, self).__init__()
        self.searchUrl = 'http://www.baidu.com/s?wd=@&pn=#&cl=3&ie=utf-8'
        self.configFile = '../fishconfig.ini'
        self.targetUrl = self.readConfig(self.configFile,'Baidu-Search','SiteUrl')
        self.pageNum = int(self.readConfig(self.configFile,'Baidu-Search','pageNum'))
        self.keyWord = self.readConfig(self.configFile,'Baidu-Search','KeyWord')
        self.searchTarget = self.searchUrl.replace('@',unicode(self.keyWord,"utf-8"))
        self.header = header
        self.header['Referer'] = 'http://www.baidu.com'

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
                sites = soup.find_all('div',id = re.compile("^\d+$"))
                for site in sites:
                    title_url[site.h3.a.get_text()] = site.h3.a.get('href')
                    id_title_url[site['id']] = title_url.copy()
                    title_url.clear()
        return  id_title_url

    def titleCompare(self,id_titleANDurl):
        '''
        '''
        print 'titleCompare'
        if os.path.exists( '../possiblesite.txt' ):
            os.remove('../possiblesite.txt')
        pen = open('../possiblesite.txt','a')
        for _id,titleANDurl in id_titleANDurl.iteritems():
            for title,url in titleANDurl.iteritems():
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
'''
    def pageCompare(self,targeturl,url):
        print 'pageCompare'
        payload = {'domain':targeturl,'domain1':url,'btnS':'查询'}
        while True:
            try:
                start = time.time()
                page = requests.post('http://tools.jzp.cc/compare/',data=payload,headers=self.header)
                print "耗时",time.time()-start
            except Exception as e:
                continue
            else:
                print '网页获取结束,开始分析'
                if page.status_code == 200:
                    text = page.content
                    try:
                        soup = BeautifulSoup(text)
                    except Exception as e:
                        print e
                    else:
                        result = soup.find('div',class_='main')
                        similar = result.find('div',id='metaresult').font.get_text()
                        break
                else:
                    continue
        print '获取比较结果'
        similar_tmp = list(similar)
        similar_tmp.pop()
        similar = ''.join(similar_tmp)
        similar = float(similar)
        print '相似度为:',similar
        if similar > 80.00:
            print '相似'
            return True
        else:
            print '不相似'
            return False
'''


if __name__=="__main__":
    baidu = Baidu_Search()
    baidu.titleCompare(baidu.pageGet())
    #baidu.pageCompare()

