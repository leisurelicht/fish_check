#! /usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import time
import random
from Common import config
from Common import function as fun
from Common import network as net

reload(sys)
sys.setdefaultencoding('utf8')


class BingSearch(object):
    """docstring for Bing_Search"""
    def __init__(self, config_file):
        super(BingSearch, self).__init__()

        self.configFile = config_file
        self.white_Domain = fun.read_config(self.configFile, 'Bing-Search', 'White_Domain').split(',')
        self.pageNum = int(fun.read_config(self.configFile, 'Bing-Search', 'Page_Num'))
        self.Search_KeyWord = fun.read_config(self.configFile, 'Bing-Search', 'Search_KeyWord').split(',')
        self.Compare_KeyWord = fun.read_config(self.configFile, 'Bing-Search', 'Compare_Title')

        self.searchUrl = 'http://cn.bing.com/search?q=@&go=提交&first=#'
        self.searchTargetlist = []
        for keyword in self.Search_KeyWord:
            self.searchTargetlist.append(self.searchUrl.replace('@', keyword))

        self.header = config.header
        self.header['Referer'] = 'http://cn.bing.com/'
        # self.header['host'] = 'cn.bing.com'

    def page_get(self):
        """
        获取页面
        返回格式为{url:[title],}格式的数据
        """
        print "page_get"
        urls_search = []
        result = {}
        title_result = []
        for searchTarget in self.searchTargetlist:
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

    def title_get(self, url_title):
        """
        获取url链接内的网站标题
        返回格式为{url:[title1,title2],url:[title1,title2]}的数据
        :param url_title:
        """
        print 'title_get'
        url_titles = {}
        for url, title_list in url_title.iteritems():
            url = fun.url_check(url)
            if url:
                connect, page = net.data_soup(url, self.header)
                if page:
                    if page.title:
                        title_list.append(page.title.get_text().strip())
                        url_titles[connect.url]=title_list
                    else:
                        print "无法获取当前URL的网页标题:"+url
                        continue
                else:
                    print "页面不存在:"+url
                    continue
            else:
                continue
        return url_titles

    def title_compare(self, total_title_and_url):
        """
        :param total_title_and_url:
        """
        print 'title_compare'
        url_and_title={}
        for url, title_list in total_title_and_url.iteritems():
            if fun.get_domain(url) not in self.white_Domain:
                if self.Compare_KeyWord in title_list[0] or self.Compare_KeyWord in title_list[-1]:
                    url_and_title[url] = title_list
            else:
                continue
        print url_and_title

if __name__ == "__main__":
    bing = BingSearch('../fishconfig.ini')
    # a = bing.data_soup('http://www.sbacn.org/')
    # print a.title
    urls = bing.page_get()
    titles = bing.title_get(urls)
    bing.title_compare(titles)

    # a= bing.url_check('http://cn.bing.com/search?q=%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C&go=Submit+Query&qs=bs&form=QBRE')
    # print a
    print time.time()
