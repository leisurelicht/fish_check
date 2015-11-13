#! /usr/bin/env python
#-*- coding=utf-8 -*-
import re
import os
import sys
import time
from Common import config
from Common import function as fun
from Common import network as net


reload(sys)
sys.setdefaultencoding('utf8')


class Baidu_Search(object):
    """docstring for Baidu_Search"""
    def __init__(self,):
        super(Baidu_Search, self).__init__()

        self.configFile = 'fishconfig.ini'
        self.targetUrl = fun.readConfig(self.configFile,'Baidu-Search','SiteUrl')
        self.pageNum = int(fun.readConfig(self.configFile,'Baidu-Search','pageNum'))
        self.Search_KeyWord = fun.readConfig(self.configFile,'Baidu-Search','Search_KeyWord')
        self.Compare_KeyWord = fun.readConfig(self.configFile,'Baidu-Search','Compare_KeyWord')

        self.searchUrl = 'http://www.baidu.com/s?wd=@&pn=#&cl=3&ie=utf-8'
        self.searchTarget = self.searchUrl.replace('@',unicode(self.Search_KeyWord,"utf-8"))

        self.header = config.header
        self.header['Referer'] = 'http://www.baidu.com'


    def pageGet(self):
        '''
        获取页面
        返回格式为{id:{title:url},}的数据
        '''
        print "pageGet"
        urls = []
        title_url = {}
        id_title_url = {}
        for num in range(1,self.pageNum+1):
            urls.append(self.searchTarget.replace('#',str((num-1)*10)))
        for url in urls:
            page = net.dataRequest(url,self.header)
            sites = page.find_all('div',id = re.compile("^\d+$"))
            for site in sites:
                title_url[site.h3.a.get_text()] = site.h3.a.get('href')
                id_title_url[site['id']] = title_url.copy()
                title_url.clear()
        return  id_title_url

    def titleGet(self,id_titleANDurl):
        '''
        '''
        for _id,titleANDurl in id_titleANDurl.iteritems():
            for title,url in titleANDurl.iteritems():
                page = net.Request(url,self.header)
                print 'baidu:',url
                if page:
                    print 'moto:',page.url
                else:
                    print 'None'
                print '*'*5


    def titleCompare(self,id_titleANDurl):
        '''
        '''
        print 'titleCompare'
        if os.path.exists( './Result/possiblesite_baidu.txt' ):
            os.remove('./Result/possiblesite_baidu.txt')
        pen = open('./Result/possiblesite_baidu.txt','a')
        for _id,titleANDurl in id_titleANDurl.iteritems():
            for title,url in titleANDurl.iteritems():
                if title == self.Compare_KeyWord:
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
    baidu.pageGet()
    #baidu.titleCompare(baidu.pageGet())
    #baidu.pageCompare()

