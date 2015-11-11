#! /usr/bin/env python
#-*- coding=utf-8 -*-

from SearchEngine import baidu
from SearchEngine import bing


if __name__=="__main__":
    bd = baidu.Baidu_Search()
    bd.titleCompare(bd.pageGet())
    bi = bing.Bing_Search()
    urls = bi.pageGet()
    titles=bi.titleGet(urls)
    bi.titleCompare(titles)



