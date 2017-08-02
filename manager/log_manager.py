# -*- coding: utf-8 -*-
import shutil, time, sys, os
import constant as const
import logging
import singleton

# Singleton class --> there is only one log manager


class LogManager():
    __metaclass__ = singleton.SingletonInstane

    res_logger = None
    info_logger = None
    err_logger = None

    def __init__(self):
        super(LogManager, self).__init__()

        path = const.MAIN_DIR
        path = path + '/logs/'
        now = time.localtime()
        today = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        res_file = path + "/" + today + "_result.txt"
        all_file = path + "/" + today + "_all.txt"
        info_file = path + "/" + today + "_info.txt"
        err_file = path + "/" + today + "_error.txt"

        if not os.path.exists(path):
            os.makedirs(path)

        self.res_logger = logging.getLogger('result_logger')
        self.info_logger = logging.getLogger('info_logger')
        self.err_logger = logging.getLogger('error_logger')

        date_format = "%b %d %H:%M:%S"
        log_format = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s"
        formatter = logging.Formatter(log_format, date_format)

        self.res_logger.addHandler(logging.FileHandler(all_file, encoding='utf-8').setFormatter(formatter))
        self.info_logger.addHandler(logging.FileHandler(all_file, encoding='utf-8').setFormatter(formatter))
        self.err_logger.addHandler(logging.FileHandler(all_file, encoding='utf-8').setFormatter(formatter))

        self.res_logger.addHandler(logging.FileHandler(res_file, encoding='utf-8').setFormatter(formatter))
        self.info_logger.addHandler(logging.FileHandler(info_file, encoding='utf-8').setFormatter(formatter))
        self.err_logger.addHandler(logging.FileHandler(err_file, encoding='utf-8').setFormatter(formatter))

        self.res_logger.addHandler(logging.StreamHandler().setFormatter(formatter))
        self.info_logger.addHandler(logging.StreamHandler().setFormatter(formatter))
        self.err_logger.addHandler(logging.StreamHandler().setFormatter(formatter))

        self.info_logger.setLevel(logging.DEBUG)
        self.res_logger.setLevel(logging.INFO)
        self.err_logger.setLevel(logging.ERROR)

        print("init singleton class")

    def get_logger(self):
        return self.info_logger, self.res_logger, self.err_logger

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())