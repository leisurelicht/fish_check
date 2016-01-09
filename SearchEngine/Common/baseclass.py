#! /usr/bin/env python
# -*- coding=utf-8 -*-

from Common import database as db

class base(object):
    """

    """
    def __init__(self,):
        super(base, self).__init__()
        self.connect = None


    def into_database(self, ut_list=None, url=None):
        """
        对URL查重后,存入数据库
        :param self:
        :param connect:
        :param ut_list:
        :param url:
        :return:
        """
        print 'into_database'
        print self.connect
        if ut_list:
            for tmp in ut_list:
                if not db.is_url_exist(self.connect, tmp['URL']):
                    db.insert_data(self.connect, tmp)
                else:
                    continue
        elif url:
            print url
            temp={'URL':url}
            if not db.is_url_exist(self.connect, url):
                db.insert_data(self.connect, temp)
            else:
                pass
        else:
            print 'Insert Error'