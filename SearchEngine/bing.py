#! /usr/bin/env python
#-*- coding=utf-8 -*-
import os
import sys
from Common import config
from Common import function as fun
from Common import network as net


reload(sys)
sys.setdefaultencoding('utf8')

class Bing_Search(object):
    """docstring for Bing_Search"""
    def __init__(self,):
        super(Bing_Search, self).__init__()

        self.configFile = './fishconfig.ini'
        self.whiteUrl = fun.readConfig(self.configFile,'Bing-Search','WhiteUrl')
        self.pageNum = int(fun.readConfig(self.configFile,'Bing-Search','PageNum'))
        self.Search_KeyWord = fun.readConfig(self.configFile,'Bing-Search','Search_KeyWord').split(',')
        self.Compare_KeyWord = fun.readConfig(self.configFile,'Bing-Search','Compare_Title')

        self.searchUrl = 'http://cn.bing.com/search?q=@&go=提交&first=#'
        self.searchTargetlist = []
        for keyword in self.Search_KeyWord:
            self.searchTargetlist.append(self.searchUrl.replace('@',keyword))

        self.header = config.header
        self.header['Referer'] = 'http://cn.bing.com/'
        #self.header['host'] = 'cn.bing.com'

    def pageGet(self):
        '''
        获取页面
        返回格式为{url:[title],}格式的数据
        '''
        print "pageGet"
        urls_search = []
        result = {}
        title_result = []
        for searchTarget in self.searchTargetlist:
            for num in range(1,self.pageNum+1):
                urls_search.append(searchTarget.replace('#',str((num-1)*10)))
            for url in urls_search:
                url  = fun.urlCheck(url)
                if url:
                    connect , page = net.dataRequest(url,self.header)
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
                else:
                    continue
            urls_search = []
        return result

    def titleGet(self,url_title):
        '''
        获取url链接内的网站标题
        返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        '''
        print 'titleGet'
        for url,titles in url_title.iteritems():
            url  = fun.urlCheck(url)
            if url:
                connect , page = net.dataRequest(url,self.header)
                if page:
                    if page.title:
                        titles.append(page.title.get_text())
                    else:
                        print "no title:"+url
                        continue
                else:
                    print "none:"+url
                    continue
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
        for url,titles in total_titleANDurl.iteritems():
            if self.Compare_KeyWord == titles[0] or self.Compare_KeyWord == titles[-1]:
                if not fun.urlCompare(url,self.whiteUrl):
                    continue
                else:
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
