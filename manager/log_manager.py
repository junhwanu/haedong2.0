# -*- coding: utf-8 -*-
import shutil, time, sys, os
import logging
import logging.handlers

def get_error_msg(err):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return ("%s %s %s %s" % (err, exc_type, fname, exc_tb.tb_lineno))

class Log():

    res_file = ""
    all_file = ""
    info_file = ""
    err_file = ""

    res_logger = None
    info_logger = None
    err_logger = None

    def init(self, path):

        path = path + '/logs/'

        now = time.localtime()
        today = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        self.res_file = path + "/" + today + "_result.txt"
        self.all_file = path + "/" + today + "_all.txt"
        self.info_file = path + "/" + today + "_info.txt"
        self.err_file = path + "/" + today + "_error.txt"

        if not os.path.exists(path):
            os.makedirs(path)

        self.res_logger = logging.getLogger('result_logger')
        self.info_logger = logging.getLogger('info_logger')
        self.err_logger = logging.getLogger('error_logger')

        DATE_FORMAT = "%b %d %H:%M:%S"
        LOG_FORMAT = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s"
        fomatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        all_fileHandler = logging.FileHandler(self.all_file, encoding='utf-8')
        all_fileHandler.setFormatter(fomatter)

        res_fileHandler = logging.FileHandler(self.res_file, encoding='utf-8')
        res_fileHandler.setFormatter(fomatter)
        res_streamHandler = logging.StreamHandler()
        res_streamHandler.setFormatter(fomatter)

        info_fileHandler = logging.FileHandler(self.info_file, encoding='utf-8')
        info_fileHandler.setFormatter(fomatter)
        info_streamHandler = logging.StreamHandler()
        info_streamHandler.setFormatter(fomatter)

        err_fileHandler = logging.FileHandler(self.err_file, encoding='utf-8')
        err_fileHandler.setFormatter(fomatter)
        err_streamHandler = logging.StreamHandler()
        err_streamHandler.setFormatter(fomatter)

        self.info_logger.addHandler(info_fileHandler)
        self.info_logger.addHandler(all_fileHandler)
        self.info_logger.addHandler(info_streamHandler)

        self.res_logger.addHandler(res_fileHandler)
        self.res_logger.addHandler(all_fileHandler)
        self.res_logger.addHandler(res_streamHandler)

        self.err_logger.addHandler(err_fileHandler)
        self.err_logger.addHandler(all_fileHandler)
        self.err_logger.addHandler(err_streamHandler)

        self.info_logger.setLevel(logging.DEBUG)
        self.res_logger.setLevel(logging.INFO)
        self.err_logger.setLevel(logging.ERROR)

    def get_logger(self):
        self.res_logger = logging.getLogger('result_logger')
        self.info_logger = logging.getLogger('info_logger')
        self.err_logger = logging.getLogger('error_logger')

        return self.info_logger, self.res_logger, self.err_logger
