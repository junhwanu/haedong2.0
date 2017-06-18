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

import log_manager as log
from constant import *
import kiwoom

if __name__ == "__main__":
    log.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))

    log.info("실제투자(1), 테스트(2)")

    while(True):
        MODE = int(input())


        if MODE is REAL:
            kw_api = kiwoom.Api()

            break
        elif MODE is TEST:
            break

        log.info("다시 입력해주세요.")