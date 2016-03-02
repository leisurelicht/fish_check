#! /usr/bin/env python
# -*- coding=utf-8 -*-

import argparse
import threading
import time
from SearchEngine import baidu
from SearchEngine import bing
from SearchEngine.Common import function as fun

def start(ob):
    tmp = ob.page_get()
    tmp = ob.title_get(tmp)
    tmp = ob.title_compare(tmp)
    ob.into_database(tmp)

def hello():
    print 'hello'

if __name__ == "__main__":
    sections = fun.read_all_section('./fishconfig.ini')
    search_list = []
    for i in sections:
        search_list.append(baidu.BaiduSearch(i))
        search_list.append(bing.BingSearch(i))

    while 1:
        print "Program start..."
        for i in search_list:
            t = threading.Thread(target=start(i))
            t.start()
        print "Program waiting..."
        time.sleep(3600)


