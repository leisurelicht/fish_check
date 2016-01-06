#! /usr/bin/env python
#-*- coding=utf-8 -*-

import argparse
from SearchEngine import baidu
from SearchEngine import bing

if __name__=="__main__":
    bd = baidu.BaiduSearch()
    bd.title_compare(bd.page_get())
    bi = bing.BingSearch()
    urls = bi.page_get()
    titles=bi.title_get(urls)
    bi.title_compare(titles)
