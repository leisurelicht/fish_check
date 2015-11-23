#! /usr/bin/env python
#-*- coding=utf-8 -*-

import argparse
from SearchEngine import baidu
from SearchEngine import bing

def Welcome():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baidu",help='Use baidu to search Phishing sites')
    args = parser.parse_args()
    print args.echo




if __name__=="__main__":
    #Welcome()
    bd = baidu.Baidu_Search()
    bd.titleCompare(bd.pageGet())
    bi = bing.Bing_Search()
    urls = bi.pageGet()
    titles=bi.titleGet(urls)
    bi.titleCompare(titles)



