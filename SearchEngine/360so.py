#! /usr/bin/env python
# -*- coding=utf-8 -*-

from Common import config
from Common import function as fun
from Common import network as net
from Common import database as db
from Common import baseclass

class SoSearch(baseclass.base):
    """
    360so search
    """
    def __init__(self, configSection):
        super(SoSearch, self).__init__(configSection)
        self.searchUrl = "http://www.so.com/s?ie=utf-8&src=360sou_newhome&q=@&pn=#"
        self.search_Target_list = []
        for keyword in self.Search_KeyWord:
            self.search_Target_list.append(self.searchUrl.replace('@', unicode(keyword,'utf-8')))

            self.header = config.header
            self.header['Referer'] = 'heep://www.sogou.com'
            self.connect = db.connect_so()

    def page_get(self):
        """
        get search page
        :return: data format {title:url}
        """
        print '360so_page_get'
        urls = []
        url_title = {}
        for searchTarget in self.search_Target_list:
            for num in range(1,self.pageNum+1):
                urls.append(searchTarget.replace('#',str(num)))
            for url in urls:
                connect, page = net.data_soup(url, self.header)
                if page:
                    sites = page.find_all('h3',class_='res-title')
                    if sites:
                        for site in sites:
                            url_title[site.a.get('href')] = site.a.get_text()
                    else:
                        print 'No result'
                        continue
                else:
                    print 'can not get 360so search result'
        return url_title

    def title_get(self, url_title):
        """

        :param url_title:
        :return: 返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        """
        print "title_get"
        url_and_title = []
        url_and_title_temp = {}
        for url, title in url_title.iteritems():
            #print "url1:", url
            connect, page = net.data_soup(url, self.header)
            if connect:
                if page:
                    if page.title:
                        #print "url2:", connect.url
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

    def title_compare(self, total_url_and_title):
        """

        :param total_url_and_title:
        :return: format data like [{url:xxx,title1:xxx,title2:xxx}]
        """
        print "title_compare"
        url_and_title = []
        for url_and_title_temp in total_url_and_title:
            if fun.get_domain(url_and_title_temp['URL']) not in self.white_Domain:
                # print 'Title1:', url_and_title_temp['TITLE1']
                # print 'Title2:', url_and_title_temp['TITLE2']
                # print 'Key:', self.Compare_KeyWord
                if self.Compare_KeyWord == url_and_title_temp['TITLE1'] or \
                                self.Compare_KeyWord == url_and_title_temp['TITLE2']:
                    url_and_title.append(url_and_title_temp.copy())
            else:
                continue
        print url_and_title
        return url_and_title

if __name__ == "__main__":
    so = SoSearch('Target5')
    tmp = so.page_get()
    tmp = so.title_get(tmp)
    tmp = so.title_compare(tmp)
    so.into_database(tmp)

