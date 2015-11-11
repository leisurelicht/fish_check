#! /usr/bin/env python
#-*- coding=utf-8 -*-

from SearchEngine import baidu


if __name__=="__main__":
    bd = baidu.Baidu_Search()
    bd.titleCompare(bd.pageGet())




