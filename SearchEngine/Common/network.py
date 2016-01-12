#! /usr/bin/env python
# -*- coding=utf-8 -*-
# 本文件保存共用的网络函数

import chardet
import requests
import config
from bs4 import BeautifulSoup
import function as fun


def data_request(url, header):
    """
    获取网页后不处理
    返回一个requests类型的连接
    出错返回一个None
    :param header:
    :param url:
    """
    print 'data_request'
    flag = fun.ssl_judge(url)
    count = 0
    while True:
        try:
            page = requests.get(url,
                                headers=header,
                                timeout=10,
                                verify=flag)
        except requests.exceptions.ConnectTimeout:
            print 'ConnectTimeout'
            if count > 1:
                return None
            else:
                count += 1
                continue
        except requests.exceptions.SSLError:
            print 'SSLError'
            flag = False
            continue
        except requests.exceptions.ConnectionError:
            print 'ConnectionError'
            if flag:
                flag = False
                count += 1
                continue
            if count > 1:
                return None
            else:
                count += 1
                continue
        except requests.exceptions.ReadTimeout:
            print 'ReadTimeout'
            if count > 1:
                return None
            else:
                count += 1
                continue
        except requests.exceptions.Timeout:  # this is important
            print 'Timeout'
            return None
        except requests.exceptions.TooManyRedirects:
            print 'TooManyRedirects'
            return None
        except requests.exceptions.HTTPError:
            print 'HTTPError'
            return None
        except requests.exceptions as e:
            error_text = fun.exception_format(fun.get_current_function_name(), e)
            print error_text
            return None
        else:
            if page.status_code == requests.codes.ok:
                return page  # get page content
            else:
                error_text = "Page Code %s " % page.status_code
                print error_text
                if count > 1:
                    return None
                else:
                    count += 1
                    continue


def data_soup(url, header):
    """
    获取网页后用BeautifulSoup处理
    返回一个元组(request格式的对象,beautifulSoup格式的对象)
    :return:
    :param url:
    :param header:
    """
    print 'data_soup'
    connect = data_request(url, header)
    try:
        if connect:
            html = connect.content
            # encoding = chardet.detect(html)
            # print encoding
            soup = BeautifulSoup(html, 'html5lib')
        else:
            return None, None
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
        return connect, None
    else:
        # print 'soup:'+soup.original_encoding
        return connect, soup

if __name__ == "__main__":
    # con = data_request('http://download1.bankofshanghai.com/kjxzdoc/ocx/mobile.pdf')
    # con = data_request('http://www.baidu.com')
    a, con = data_soup('http://www.kukud.net/meinv/html/2928.asp', config.header)
    print a.url
    print a.history
    print a.headers
    print con
    # print con.url
    # print con.encoding
    # for k,v in con.headers.iteritems():
    #   print k + ':' + v
    # if 'text' not in con.headers['content-type']:
    #    print 'error'
