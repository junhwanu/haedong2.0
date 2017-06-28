# -*- coding: utf-8 -*-
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/modules');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/constant');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/manager');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/net');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/simulate');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/chart');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/var');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/viewer');

import log_manager
import constant as const
import tester
import kiwoom
import db_manager as dbm

if __name__ == "__main__":

    logger = log_manager.Log()
    logger.init(const.MAIN_DIR)
    log, res, err_log = logger.get_logger()

    log.info("실제투자(1), 테스트(2)")
    while(True):
        const.MODE = int(input())

        if const.MODE is const.REAL:
            kw_api = kiwoom.Api()

            break
        elif const.MODE is const.TEST:
            tester.proc()
            break

        print("다시 입력해주세요.")