# -*- coding: utf-8 -*-

import logging
import os
import time

from constant import constant_ as const
from utils.singleton import Singleton


# Singleton class --> there is only one log manager

class LogManager(metaclass=Singleton):
    res_logger, info_logger, err_logger = None, None, None
    
    def __init__(self):
        path = const.MAIN_DIR
        path = path + '/logs/'
        now = time.localtime()
        today = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        res_file = path + "/" + today + "_result.txt"
        all_file = path + "/" + today + "_all.txt"
        info_file = path + "/" + today + "_info.txt"
#         err_file = path + "/" + today + "_error.txt"

        if not os.path.exists(path):
            os.makedirs(path)

        self.res_logger = logging.getLogger('result_logger')
        self.info_logger = logging.getLogger('info_logger')
        self.err_logger = logging.getLogger('error_logger')

        date_format = "%b %d %H:%M:%S"
        log_format = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s"
        formatter = logging.Formatter(log_format, date_format)

        all_file_handler = logging.FileHandler(all_file, encoding='utf-8')
        all_file_handler.setFormatter(formatter)

        res_file_handler = logging.FileHandler(res_file, encoding='utf-8')
        res_file_handler.setFormatter(formatter)
        res_stream_handler = logging.StreamHandler()
        res_stream_handler.setFormatter(formatter)

        info_file_handler = logging.FileHandler(info_file, encoding='utf-8')
        info_file_handler.setFormatter(formatter)
        info_stream_handler = logging.StreamHandler()
        info_stream_handler.setFormatter(formatter)

        self.info_logger.addHandler(info_file_handler)
        self.info_logger.addHandler(all_file_handler)
        self.info_logger.addHandler(info_stream_handler)

        self.res_logger.addHandler(res_file_handler)
        self.res_logger.addHandler(all_file_handler)
        self.res_logger.addHandler(res_stream_handler)

        self.info_logger.setLevel(logging.DEBUG)
        # self.info_logger.setLevel(logging.INFO)
        self.res_logger.setLevel(logging.INFO)
        print("Initialize Log Manager")

    def get_logger(self):
        return self.info_logger, self.res_logger, self.err_logger

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())