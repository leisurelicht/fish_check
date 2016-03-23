#! /usr/bin/env python
# -*- coding=utf-8 -*-

import os
import database as db
import function as fun


class base(object):
    """

    """
    def __init__(self,configSection):
        super(base, self).__init__()
        path = os.getcwd()
        sub = path.find('fish_check')
        path = path[sub:]
        name = path.split('/')
        if len(name) == 1:
            self.configFile = './fishconfig.ini'
        elif len(name) == 2:
            self.configFile = '../fishconfig.ini'
        elif len(name) == 3:
            self.configFile = '../../fishconfig.ini'
        else:
            self.configFile = None

        self.white_Domain = fun.read_config(self.configFile, configSection, 'White_Domain').split(',')
        #self.pageNum = int(fun.read_config(self.configFile, configSection, 'Page_Num'))
        self.pageNum = int(fun.read_config(self.configFile, configSection, 'PageNum').strip())
        self.Search_KeyWord = fun.read_config(self.configFile, configSection, 'Search_KeyWord').split(',')
        self.Compare_KeyWord = fun.read_config(self.configFile, configSection, 'Compare_Title')

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
                temp={'URL':ut, 'READ':'NO'}
                if not db.is_url_exist(self.connect, ut):
                    db.insert_data(self.connect, temp)
            elif isinstance(ut, dict):
                ut['Read'] = 'NO'
                if not db.is_url_exist(self.connect, ut['URL']):
                    db.insert_data(self.connect, ut)
            elif isinstance(ut, list):
                for tmp in ut:
                    tmp['Read'] = 'NO'
                    if not db.is_url_exist(self.connect, tmp['URL']):
                        db.insert_data(self.connect, tmp)
                    else:
                        continue
            else:
                print "ERROR TYPE"

    def clear_database(self):
        """
        清空数据库
        :return:
        """
        db.remove_date(self.connect)

    def jud_white(self,url):
        if fun.get_domain(url) in self.white_Domain:
            return True
        else:
            return False


if __name__ == "__main__":
    base = base('Target2')