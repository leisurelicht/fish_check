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
            #self.connect = db.connect_sogou()

    def title_and_url(self,tag):
        return tag
        # return tag['class'] == 'vrTitle'

    def page_get(self):
        """
        get search page
        :return: data format {id:{title:url}}
        """
        print "sogou_page_get"
        urls = []
        title_url = {}
        id_title_url = {}
        id_sign = 1
        for searchTarget in self.search_Target_list:
            for num in range(1, self.pageNum+1):
                urls.append(searchTarget.replace('#', str(num)))
            for url in urls:
                connect, page = net.data_soup(url, self.header)
                if page:
                    result = page.find_all(self.title_and_url)
                    print result
                    if result:
                        pass
                        # site= result.find_all('h3')
                        # if site:
                        #     print site.get_text()
                    else:
                        print 'No result'
                        continue
                else:
                    print 'can not get sogou search result'
if __name__ == "__main__":
    sogou = SogouSearch('Target2')
    tmp = sogou.page_get()