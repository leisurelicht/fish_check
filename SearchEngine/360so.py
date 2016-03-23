#! /usr/bin/env python
# -*- coding=utf-8 -*-

from Common import config
from Common import function as fun
from Common import network as net
from Common import database as db
from Common import baseclass

class SoSearch(baseclass.base):
    """
    360so search
    """
    def __init__(self, configSection):
        super(SoSearch, self).__init__(configSection)
        self.searchUrl = "http://www.so.com/s?ie=utf-8&src=360sou_newhome&q=@&pn=#"