#! /usr/bin/env python
#-*- coding=utf-8 -*-
import re
import os
import sys
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
        self.whiteUrl = fun.readConfig(self.configFile,'Baidu-Search','WhiteUrl')
        self.pageNum = int(fun.readConfig(self.configFile,'Baidu-Search','PageNum'))
        self.Search_KeyWord = fun.readConfig(self.configFile,'Baidu-Search','Search_KeyWord').split(',')
        self.Compare_KeyWord = fun.readConfig(self.configFile,'Baidu-Search','Compare_Title')

        self.searchUrl = 'http://www.baidu.com/s?wd=@&pn=#&cl=3&ie=utf-8&nojc=1'
        self.searchTargetlist = []
        for keyword in self.Search_KeyWord:
            self.searchTargetlist.append(self.searchUrl.replace('@',unicode(keyword,"utf-8")))

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
        id_sign = 1
        for searchTarget in self.searchTargetlist:
            print searchTarget
            for num in range(1,self.pageNum+1):
                urls.append(searchTarget.replace('#',str((num-1)*10)))
            for url in urls:
                print url
                connect , page = net.dataRequest(url,self.header)
                sites = page.find_all('div',id = re.compile("^\d+$"))
                for site in sites:
                    if site:
                        title_url[site.h3.a.get_text()] = site.h3.a.get('href')
                        #id_title_url[site['id']] = title_url.copy()
                        id_title_url[id_sign] = title_url.copy()
                        id_sign += 1
                        title_url.clear()
                    else:
                        continue
            urls = []
        #for id_tmp,title_url in id_title_url.iteritems():
        #    for title,url in title_url.iteritems():
        #        print "id:" + str(id_tmp)
        #        print 'title:' + title
        #        print 'url:' + url
        return  id_title_url

    def titleGet(self,id_titleANDurl):
        '''
        '''
        for id_tmp,titleANDurl in id_titleANDurl.iteritems():
            for title,url in titleANDurl.iteritems():
                connect , page = net.dataRequest(url,self.header)
                print 'baidu:',url
                if connect:
                    print 'moto:',connect.url
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
                    if not fun.urlCompare(url,self.whiteUrl):
                        continue
                    else:
                        pen.write('url:'+url+'\n')
                        pen.write('***********'+'\n')
                        pen.flush()
                    #if self.pageCompare(self.whiteUrl,url):
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
    def pageCompare(self,whiteUrl,url):
        print 'pageCompare'
        payload = {'domain':whiteUrl,'domain1':url,'btnS':'查询'}
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

