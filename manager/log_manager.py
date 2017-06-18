# -*- coding: utf-8 -*-
import shutil, time, sys, os
import logging

res_logger = None
info_logger = None
all_logger = None

def init(path):
    global res_logger, info_logger, all_logger

    path = path + '/logs/'
    now = time.localtime()
    today = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

    res_file = path + "/" + today + "_result.txt"
    all_file = path + "/" + today + "_all.txt"
    info_file = path + "/" + today + "_info.txt"

    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.isfile(res_file) == False:
        file = open(res_file, 'w')
        file.close()

    if os.path.isfile(all_file) == False:
        file = open(all_file, 'w')
        file.close()

    if os.path.isfile(info_file) == False:
        file = open(info_file, 'w')
        file.close()

    res_logger = logging.getLogger('result_logger')
    info_logger = logging.getLogger('info_logger')
    all_logger = logging.getLogger('all_logger')

    DATE_FORMAT = "%b %d %H:%M:%S"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s"
    fomatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    all_fileHandler = logging.FileHandler(all_file, encoding='utf-8')
    all_streamHandler = logging.StreamHandler()

    all_fileHandler.setFormatter(fomatter)
    all_streamHandler.setFormatter(fomatter)

    res_fileHandler = logging.FileHandler(res_file, encoding='utf-8')
    res_fileHandler.setFormatter(fomatter)

    info_fileHandler = logging.FileHandler(info_file, encoding='utf-8')
    info_fileHandler.setFormatter(fomatter)

    info_logger.addHandler(info_fileHandler)
    res_logger.addHandler(res_fileHandler)
    all_logger.addHandler(all_fileHandler)
    all_logger.addHandler(all_streamHandler)
    all_logger.setLevel(logging.DEBUG)
    info_logger.setLevel(logging.INFO)
    res_logger.setLevel(logging.INFO)


def info(log_msg):
    all_logger.info(log_msg)
    info_logger.info(log_msg)

def debug(log_msg):
    all_logger.debug(log_msg)
    info_logger.info(log_msg)

def warning(log_msg):
    all_logger.warning(log_msg)
    info_logger.info(log_msg)

def error(log_msg):
    all_logger.error(log_msg)
    info_logger.info(log_msg)

def critical(log_msg):
    all_logger.critical(log_msg)
    info_logger.info(log_msg)

def result(log_msg):
    all_logger.info(log_msg)
    res_logger.info(log_msg)