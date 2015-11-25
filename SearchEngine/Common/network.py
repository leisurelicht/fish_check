#! /usr/bin/env python
#-*- coding=utf-8 -*-
#本文件保存共用的网络函数

import sys
import chardet
import requests
import config
from bs4 import BeautifulSoup
import function as fun




#页面读取函数,その１
def Request(url,header):
    '''
    获取网页后不处理
    返回一个requests类型的连接
    出错返回一个None
    '''
    print 'Request'
    flag = fun.sslJudge(url)
    count = 0
    while True:
        try:
            page = requests.get( url , headers = header, timeout = 10 , verify = flag )
        except requests.exceptions.ConnectionError:
            print 'ConnectionError'
            if flag == True:
                flag = False
                count += 1
                continue
            if count > 1:
                return None
            else:
                count += 1
                continue
        except requests.exceptions.Timeout:#this is important
            print 'Timeout'
            return None
        except requests.exceptions.ConnectTimeout:
            print 'ConnectTimeout'
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
        except requests.exceptions.TooManyRedirects:
            print 'TooManyRedirects'
            return None
        except requests.exceptions.SSLError:
            print 'SSLError'
            flag = False
            continue
        except requests.exceptions.HTTPError:
            print 'HTTPError'
            return None
        except requests.exceptions as e:
            errortext = "Error in function requests: \" %s \" ,\n \
                Error name is : \" %s \" ,\n \
                Error type is : \" %s \" ,\n \
                Error Message is : \" %s \" ,\n \
                Error doc is : \" %s \" \n" % \
            (sys._getframe().f_code.co_name,\
                 e.__class__.__name__,\
                 e.__class__,\
                 e,\
                 e.__class__.__doc__)
            print errortext
            return None
        else:
            if page.status_code == requests.codes.ok:
                return page #get page content
                break
            else:
                errortext = "Page Code %s " % page.status_code
                print errortext
                if count > 1:
                    return None
                else:
                    count += 1
                    continue




#页面读取函数、その２
def dataRequest(url,header):
    '''
    获取网页后用BeautifulSoup处理
    返回一个元组(request格式的对象,beautifulsoup格式的对象)
    '''
    print 'dataRequest'
    page = Request(url,header)
    try:
        if page:
            html = page.content
            #encoding = chardet.detect(html)
            #print encoding
            soup = BeautifulSoup(html,'html5lib')#,from_encoding=encoding['encoding'])
        else:
            return (None,None)
    except Exception as e:
        errortext = "Error in function soup: \" %s \" ,\n \
                Error name is : \" %s \" ,\n \
                Error type is : \" %s \" ,\n \
                Error Message is : \" %s \" ,\n \
                Error doc is : \" %s \" \n" % \
                (sys._getframe().f_code.co_name,\
                 e.__class__.__name__,\
                 e.__class__,\
                 e,\
                 e.__class__.__doc__)
        print errortext
        return (page,None)
    else:
        print 'soup:'+soup.original_encoding
        return (page,soup)

if __name__ == "__main__":
    #con = Request('http://download1.bankofshanghai.com/kjxzdoc/ocx/mobile.pdf')
    #con = Request('http://www.baidu.com')
    a , con = dataRequest('http://www.kukud.net/meinv/html/2928.asp',config.header)
    print a.url
    print a.history
    print a.headers
    print con.head.title
    #print con.url
    #print con.encoding
    #for k,v in con.headers.iteritems():
    #   print k + ':' + v
    #if 'text' not in con.headers['content-type']:
    #    print 'error'

