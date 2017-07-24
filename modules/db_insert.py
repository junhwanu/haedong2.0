# -*- coding: utf-8 -*-
from __module import ModuleClass


class DBInsert(ModuleClass):
    def __init__(self):
        super(DBInsert, self).__init__()
        pass

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())