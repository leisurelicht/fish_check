#! /usr/bin/env python
# -*- coding=utf-8 -*-

from Common import database as db

class base(object):
    """

    """
    def __init__(self,):
        super(base, self).__init__()
        self.connect = None


    def into_database(self, ut=None):
        """
        对URL查重后存入数据库
        :param ut: url and title
        :return:
        """
        print 'into_database'
        if ut:
            if isinstance(ut, str):
                temp={'URL':ut}
                if not db.is_url_exist(self.connect, ut):
                    db.insert_data(self.connect, temp)
            elif isinstance(ut, dict):
                if not db.is_url_exist(self.connect, ut['URL']):
                    db.insert_data(self.connect, ut)
            elif isinstance(ut, list):
                for tmp in ut:
                    if not db.is_url_exist(self.connect, tmp['URL']):
                        db.insert_data(self.connect, tmp)
                    else:
                        continue
            else:
                print "ERROR TYPE"
