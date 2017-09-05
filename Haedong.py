# -*- coding: utf-8 -*-

import sys, time
from modules import kiwoom, health_server, destroy_python
from constant import constant_ as const
from simulate import tester
from manager.log_manager import LogManager

# import simulate.tester as tester
# import constant.constant_ as const
# import modules.kiwoom as kiwoom
# import modules.health_server as health_server

# from manager.log_manager import LogManager
# import strategy.para as para
# import chart_manager as chart


class Haedong(object):
    running_time = 0
    log, res, err_log = None, None, None

    def __init__(self):
        super(Haedong, self).__init__()
        self.log, self.res, self.err_log = LogManager().get_logger()

    def run(self):
        s_time = time.time()

        while True:
            if len(sys.argv) == 1:
                self.log.info("실제투자(1), 테스트(2)")
                const.MODE = int(input())
            else:
                const.MODE = int(sys.argv[1])

            if const.MODE is const.REAL:
                #파이썬 프로그램 종료 기능
                destroy_python.Destroy_python()
                
                # health server run
                health_server_thread = health_server.HealthConnectManager()
                health_server_thread.start()
                
                kiwoom.Api()
            
                health_server_thread.server_close()
                health_server_thread.join(timeout=5)
                self.log.info("헬스 체크서버 종료")
                
                break

            elif const.MODE is const.TEST:
                test = tester.Tester()
                test.proc()
                break

            print("다시 입력해주세요.")

        self.log.info("Haedong 프로그램이 종료됩니다.")
        sys.exit()
        
        '''
        self.running_time = time.time() - s_time

        self.log.info("Total running time : %s" % self.running_time)
        #    log.info("chart_manager running time : %s, %s%s" % (chart.running_time, round(chart.running_time * 100 / running_time, 2), '%'))
        self.log.info(
            "para running time : %s, %s%s" % (para.running_time, round(para.running_time * 100 / self.running_time, 2), '%'))
        self.log.info("db test running time : %s, %s%s" % (
        tester.running_time, round(tester.running_time * 100 / self.running_time, 2), '%'))
        '''


if __name__ == "__main__":
    headong = Haedong()
    headong.run()