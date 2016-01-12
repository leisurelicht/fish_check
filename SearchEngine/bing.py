#! /usr/bin/env python
# -*- coding=utf-8 -*-

import sys
from Common import config
from Common import function as fun
from Common import network as net
from Common import database as db
from Common import baseclass

reload(sys)
sys.setdefaultencoding('utf8')


class BingSearch(baseclass.base):
    """docstring for Bing_Search"""
    def __init__(self, config_file):
        super(BingSearch, self).__init__()
        # self.configFile = config_file
        # self.white_Domain = fun.read_config(self.configFile, 'Bing-Search', 'White_Domain').split(',')
        # self.pageNum = int(fun.read_config(self.configFile, 'Bing-Search', 'Page_Num'))
        # self.Search_KeyWord = fun.read_config(self.configFile, 'Bing-Search', 'Search_KeyWord').split(',')
        # self.Compare_KeyWord = fun.read_config(self.configFile, 'Bing-Search', 'Compare_Title')

        self.searchUrl = 'http://cn.bing.com/search?q=@&go=提交&first=#'
        self.searchTarget_list = []
        for keyword in self.Search_KeyWord:
            self.searchTarget_list.append(self.searchUrl.replace('@', keyword))

        self.header = config.header
        self.header['Referer'] = 'http://cn.bing.com/'
        # self.header['host'] = 'cn.bing.com'
        self.connect = db.connect_bing()

    def page_get(self):
        """
        获取页面
        返回格式为{url:[title],}格式的数据
        """
        print "page_get"
        urls_search = []
        result = {}
        for searchTarget in self.searchTarget_list:
            for num in range(1, self.pageNum+1):
                urls_search.append(searchTarget.replace('#', str((num-1)*10)))
            for url in urls_search:
                url = fun.url_check(url)
                if url:
                    connect, page = net.data_soup(url, self.header)
                    if page:
                        sites = page.find_all('h2')
                        for site in sites:
                            if site.a:
                                result[site.a.get('href').strip()] = site.a.get_text().strip()
                            else:
                                continue
                    else:
                        continue
                else:
                    continue
            urls_search = []
        return result

    def title_get(self, url_title):
        """
        获取url链接内的网站标题
        返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        :param url_title:
        """
        print 'title_get'
        url_and_title = []
        url_and_title_temp = {}
        for url, title in url_title.iteritems():
            url = fun.url_check(url)
            if url:
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
                            # print "无法获取当前URL的网页标题:"+url
                            continue
                    else:
                        tmp = {'URL':connect.url, 'TYPE':'FT_ER', 'TITLE1':'无法格式化页面'}
                        self.into_database(tmp)
                        continue
                else:
                    tmp = {'URL':url, 'TYPE':'CON_ER', 'TITLE1':'无法连接'}
                    self.into_database(tmp)
                    continue
        return url_and_title

    def title_compare(self, total_url_and_title):
        """
        :param total_url_and_title:
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


if __name__ == "__main__":
    bing = BingSearch('../fishconfig.ini')
    tmp = bing.page_get()
    tmp = bing.title_get(tmp)
    tmp = bing.title_compare(tmp)
    bing.into_database(tmp)
    # bing.into_database('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    # a= bing.url_check('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    # print a
