#! /usr/bin/env python
#-*- coding=utf-8 -*-
#本文件内保存一些共用的函数

import urlparse
from ConfigParser import ConfigParser

#配置读取函数
def readConfig(iniFile,section,option):
    '''
    读取配置文件
    '''
    print 'readConfig'
    try:
        config = ConfigParser()
        config.read(iniFile)
    except Exception:
        print "无法读取配置文件"
    else:
        return config.get(section,option)

#协议判断函数
def sslJudge(url_str):
    '''
    判断url是https还是http连接
    https 返回True
    http 返回False
    '''
    print 'sslJudge'
    url = urlparse.urlparse(url_str)
    if url.scheme == 'https':
        return True
    else:
        return False

#url检查函数
def urlCheck(url_str):
    '''
    检查url是否完整
    缺协议的补为http返回
    缺域名的返回None
    '''
    print 'urlCheck'
    url = urlparse.urlsplit(url_str)
    if url.netloc == '':
        return None
    else:
        if url.scheme == '':
            url.scheme == 'http'
            return urlparse.urlunsplit(url)
        else:
            return url_str
