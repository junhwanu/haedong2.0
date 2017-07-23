# -*- coding: utf-8 -*-
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/modules');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/constant');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/manager');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/net');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/simulate');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/strategy');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/chart');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/var');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/viewer');
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/config');

import log_manager
import constant as const
import tester
import kiwoom
import chart_manager as chart
import para
import health_server

running_time = 0

if __name__ == "__main__":
    s_time = time.time()

    logger = log_manager.Log()
    logger.init(const.MAIN_DIR)
    log, res, err_log = logger.get_logger()

    input()
    while(True):

        if len(sys.argv) == 1:
            log.info("실제투자(1), 테스트(2)")
            const.MODE = int(input())
        else:
            const.MODE = int(sys.argv[1])

        if const.MODE is const.REAL:
            # health server run
            health_server_thread = health_server.HealthConnectManager()
            health_server_thread.start()

            kw_api = kiwoom.Api()

            health_server_thread.close()
            health_server_thread.join(5)
            print("헬스 체크서버 종료")

            break
        elif const.MODE is const.TEST:
            tester.proc()
            break

        print("다시 입력해주세요.")

    running_time = time.time() - s_time

    log.info("Total running time : %s" % running_time)
#    log.info("chart_manager running time : %s, %s%s" % (chart.running_time, round(chart.running_time * 100 / running_time, 2), '%'))
    log.info("para running time : %s, %s%s" % (para.running_time, round(para.running_time * 100 / running_time, 2), '%'))
    log.info("db test running time : %s, %s%s" % (tester.running_time, round(tester.running_time * 100 / running_time, 2), '%'))
