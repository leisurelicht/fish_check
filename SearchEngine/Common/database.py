#! usr/bin/env python
# -*- coding=utf-8 -*-
import pymongo
import function as fun

host = "localhost"
port = 27017

def connect_bing():
    print 'connect_bing'
    try:
        client = pymongo.MongoClient(host, port)
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
    else:
        db = client.fish_check
        collection = db.bing
        return collection


def connect_baidu():
    print 'connect_bing'
    try:
        client = pymongo.MongoClient(host, port)
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
    else:
        db = client.fish_check
        collection = db.baidu
        return collection


def insert_data(collection, database):
    print 'insert_data'
    try:
        if isinstance(database, list):
            collection.insert_many(database)
        elif isinstance(database, dict):
            collection.insert_one(database)
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text


def is_url_exist(collection, url):
    print 'search_url'
    try:
        temp = collection.find({'url': url})
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
    else:
        return temp.count()


def remove_date(collection):
    collection.remove()


if __name__ == "__main__":
    con = connect_bing()
    search_url(con, 'http://www.bing.com/knows/search?q=%e4%b8%8a%e6%b5%b7%e9%93%b6%e8%a1%8c&mkt=zh-cn')
    # con.remove()
    # for data in con.find():
    #    print data['title']

    # insert_data(con, {"name":"freebuf"})
