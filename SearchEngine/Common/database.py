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
    print 'connect_baidu'
    try:
        client = pymongo.MongoClient(host, port)
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
    else:
        db = client.fish_check
        collection = db.baidu
        return collection

def connect_sogou():
    print "connect_sogou"
    try:
        client = pymongo.MongoClient(host, port)
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(),e)
        print error_text
    else:
        db = client.fish_check
        collection = db.sogou
        return collection


def insert_data(collection, database):
    """
    向数据库中插入数据
    :param collection: 数据库对象
    :param database: 可以是json格式或者dict格式的数据
    """
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
    """
    判断一个URL是否已经被存入数据库中
    存在 返回True
    不存在 返回False
    :param collection: 数据库实例对象
    :param url: url
    """
    print 'search_url'
    try:
        temp = collection.find({'url': url})
    except Exception as e:
        error_text = fun.exception_format(fun.get_current_function_name(), e)
        print error_text
    else:
        if temp.count() == 0:
            return False
        else:
            return True





def remove_date(collection):
    collection.remove()


if __name__ == "__main__":
    con = connect_bing()
    # con.remove()
    # for data in con.find():
    #    print data['title']

    # insert_data(con, {"name":"freebuf"})
