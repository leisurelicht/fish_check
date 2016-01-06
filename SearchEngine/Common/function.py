#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 本文件内保存一些共用的函数

import urlparse
import inspect
from tld import get_tld
from ConfigParser import ConfigParser


# 配置读取函数
def read_config(ini_file, section, option):
    """
    读取配置文件
    :param option:
    :param section:
    :param ini_file: 文件
    """
    print 'read_config'
    try:
        config = ConfigParser()
        config.read(ini_file)
    except Exception as e:
        print "无法读取配置文件"
        error_text = exception_format(get_current_function_name(), e)
        print error_text
    else:
        return config.get(section, option)


# 协议判断函数
def ssl_judge(url_str):
    """
    判断url是https还是http连接
    https 返回True
    http 返回False
    :param url_str: url
    """
    print 'ssl_judge'
    url = urlparse.urlparse(url_str)
    if url.scheme == 'https':
        return True
    else:
        return False


# url检查函数
def url_check(url_str):
    """
    检查url是否完整
    缺协议的补为http返回
    缺域名的返回None
    :param url_str:
    """
    print 'url_check'
    url = urlparse.urlsplit(url_str)
    if url.netloc == '':
        return None
    else:
        if url.scheme == '':
            url.scheme = 'http'
            return urlparse.urlunsplit(url)
        else:
            return url_str

def get_domain(url):
    """
    获取域名
    :param url:
    :return:
    """
    print "domain_get"
    return get_tld(url)


# url比较函数
def url_compare(url1, url2):
    """
    比较两个url的域名是否相同
    相同返回 0
    不相同返回比较值
    :param url2:
    :param url1:
    """
    print 'url_compare'
    url_one = get_tld(url1)
    url_two = get_tld(url2)
    return cmp(url_one, url_two)


def get_current_function_name():
    """
    动态的获取当前函数名
    :return: 函数名
    """
    return inspect.stack()[1][3]


def exception_format(function_name, e):
    """
    :param function_name: 抛出异常的函数名
    :param e: 异常
    :return: 格式化后的信息
    """
    error_text = "     Error in functon : \" {0:s} \" ,\n \
    Error name is : \" {1:s} \" ,\n \
    Error type is : \" {2:s} \" ,\n \
    Error Message is : \" {3:s} \" ,\n \
    Error doc is : \" {4:s} \" , \n " \
    .format(function_name,
            e.__class__.__name__,
            e.__class__,
            e,
            e.__class__.__doc__)
    return error_text

if __name__ == "__main__":
    url_compare('http://www.bankofshanghai.com',
                'https://ibank.bankofshanghai.com/eweb/vx_zh_CN/login.html?LoginType=R&_locale=zh_CN')
