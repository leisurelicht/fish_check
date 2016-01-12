#! /usr/bin/env python
# -*- coding=utf-8 -*-

import re
import sys
from Common import config
from Common import function as fun
from Common import network as net
from Common import database as db
from Common import baseclass


reload(sys)
sys.setdefaultencoding('utf8')


class BaiduSearch(baseclass.base):
    """docstring for baidu_search"""
    def __init__(self,):
        super(BaiduSearch, self).__init__()
        # self.configFile = config_file
        # self.white_Domain = fun.read_config(self.configFile, 'Baidu-Search', 'White_Domain').split(',')
        # self.pageNum = int(fun.read_config(self.configFile, 'Baidu-Search', 'Page_Num'))
        # self.Search_KeyWord = fun.read_config(self.configFile, 'Baidu-Search', 'Search_KeyWord').split(',')
        # self.Compare_KeyWord = fun.read_config(self.configFile, 'Baidu-Search', 'Compare_Title')

        self.searchUrl = 'http://www.baidu.com/s?wd=@&pn=#&cl=3&ie=utf-8&nojc=1'
        self.search_Target_list = []
        for keyword in self.Search_KeyWord:
            self.search_Target_list.append(self.searchUrl.replace('@', unicode(keyword, "utf-8")))

        self.header = config.header
        self.header['Referer'] = 'http://www.baidu.com'
        self.connect = db.connect_baidu()

    def page_get(self):
        """
        获取页面
        返回格式为{id:{title:url},}的数据
        """
        print "page_get"
        urls = []
        title_url = {}
        id_title_url = {}
        id_sign = 1
        for searchTarget in self.search_Target_list:
            for num in range(1, self.pageNum+1):
                urls.append(searchTarget.replace('#', str((num-1)*10)))
            for url in urls:
                connect, page = net.data_soup(url, self.header)
                sites = page.find_all('div', id=re.compile("^\d+$"))
                for site in sites:
                    if site:
                        if site.h3:
                            if site.h3.a:
                                title_url[site.h3.a.get_text()] = site.h3.a.get('href')
                                id_title_url[id_sign] = title_url.copy()
                                id_sign += 1
                                title_url.clear()
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
            urls = []
        return id_title_url

    def title_get(self, id_title_and_url):
        """
        :param id_title_and_url:
        """
        print 'title_get'
        url_and_title = []
        url_and_title_temp = {}
        for id_tmp, title_and_url in id_title_and_url.iteritems():
            for title, url in title_and_url.iteritems():
                connect, page = net.data_soup(url, self.header)
                if connect:
                    if page:
                        if page.title:
                            url_and_title_temp['URL'] = connect.url
                            url_and_title_temp['TITLE1'] = title
                            url_and_title_temp['TITLE2'] = page.title.get_text().strip()
                            url_and_title.append(url_and_title_temp.copy())
                            url_and_title_temp.clear()
                        else:
                            tmp = {'URL':connect.url, 'TYPE':'GET_ER', 'TITLE1':'无法获取当前URL的网页标题'}
                            self.into_database(tmp)
                            # print "无法获取当前URL的网页标题"
                            continue
                    else:
                        tmp = {'URL':connect.url, 'TYPE':'FT_ER', 'TITLE1':'无法格式化页面'}
                        self.into_database(tmp)
                        # print "无法格式化页面"
                        continue
                else:
                    tmp = {'URL':url, 'TYPE':'CON_ER', 'TITLE1':'无法连接'}
                    self.into_database(tmp)
                    # print '无法连接'
                    continue
        return url_and_title

    def title_compare(self, total_url_and_title):
        """

        :param total_url_and_title:
        :return: [{url:xxx,title1:xxx,title2:xxx}]
        """
        print 'title_compare'
        url_and_title = []
        for url_and_title_temp in total_url_and_title:
            if fun.get_domain(url_and_title_temp['URL']) not in self.white_Domain:
                if self.Compare_KeyWord == url_and_title_temp['TITLE1'] or \
                                self.Compare_KeyWord == url_and_title_temp['TITLE2']:
                    url_and_title.append(url_and_title_temp.copy())
                else:
                    continue
        return url_and_title



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


if __name__ == "__main__":
    baidu = BaiduSearch()
    tmp = baidu.page_get()
    tmp = baidu.title_get(tmp)
    tmp = baidu.title_compare(tmp)
    baidu.into_database(tmp)
    #baidu.clear_database()


    # baidu.pageCompare()

    # temp = []
    # for i in range(10):
    #     temp.append(BaiduSearch('../fishconfig.ini'))
