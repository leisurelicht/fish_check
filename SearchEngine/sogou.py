#! /usr/bin/env python
# -*- coding=utf-8 -*-

import re
import sys
from Common import config
from Common import function as fun
from Common import network as net
from Common import database as db
from Common import baseclass

class SogouSearch(baseclass.base):
    """
    sogou search
    """
    def __init__(self,configSection):
        super(SogouSearch, self).__init__(configSection)
        self.searchUrl = 'https://www.sogou.com/web?query=@&ie=utf8&page=#'
        self.search_Target_list = []
        for keyword in self.Search_KeyWord:
            self.search_Target_list.append(self.searchUrl.replace('@',unicode(keyword,'utf-8')))

            self.header = config.header
            self.header['Referer'] = 'https://www.sogou.com'
            self.cert = '/home/licht/Code/fish_check/SearchEngine/Common/sogou'
            self.connect = db.connect_sogou()

    def page_get(self):
        """
        get search page
        :return: data format {title:url}
        """
        print "sogou_page_get"
        urls = []
        url_title = {}
        for searchTarget in self.search_Target_list:
            for num in range(1, self.pageNum+1):
                urls.append(searchTarget.replace('#', str(num)))
            for url in urls:
                connect, page = net.data_soup(url, self.header)
                if page:
                    sites = page.find_all('h3',class_='pt')
                    results = page.find_all('h3',class_='vrTitle')
                    if sites or results:
                        for site in sites:
                            url_title[site.a.get('href')] = site.a.get_text()
                        for result in results:
                            url_title[result.a.get('href')] = result.a.get_text()
                    else:
                        print 'No result'
                        continue
                else:
                    print 'can not get sogou search result'
        return url_title

    def title_get(self, url_title):
        '''
        :param url_title:
        :return: 返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        '''
        print "title_get"
        url_and_title = []
        url_and_title_temp = {}
        for url, title in url_title.iteritems():
            print 'url:', url
            connect, page = net.data_soup(url, self.header)
            if connect:
                if page:
                    if page.title:
                        print connect.url
                        url_and_title_temp['URL'] = connect.url
                        url_and_title_temp['TITLE1'] = title
                        url_and_title_temp['TITLE2'] = page.title.get_text().strip()
                        url_and_title.append(url_and_title_temp.copy())
                        url_and_title_temp.clear()
                    else:
                        if not self.jud_white(connect.url):
                            tmp = {'URL':connect.url, 'TYPE':'GET_ERROR', 'TITLE1':'无法获取当前URL的网页标题'}
                            self.into_database(tmp)
                            #print "无法获取当前URL的网页标题"
                        continue
                else:
                    if not self.jud_white(connect.url):
                        tmp = {'URL':connect.url, 'TYPE':'FORMAT_ERROR', 'TITLE1':'无法格式化页面'}
                        self.into_database(tmp)
                        # print "无法格式化页面"
                    continue
            else:
                tmp = {'URL':url, 'TYPE':'CONNECT_ERRROR', 'TITLE1':'无法连接'}
                # self.into_database(tmp)
                #print '无法连接'
                continue
        return url_and_title


if __name__ == "__main__":
    sogou = SogouSearch('Target5')
    tmp = sogou.page_get()
    tmp = sogou.title_get(tmp)
    tmp = sogou.title_compare(tmp)
    sogou.into_database(tmp)