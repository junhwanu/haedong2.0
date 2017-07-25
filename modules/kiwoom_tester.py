# -*- coding: utf-8 -*-

import chart_manager as ctm
import log_manager
import strategy_manager as stm
from __module import ModuleClass

log = None
res = None
err_log = None

class KiwoomTester(ModuleClass):
    chart = None
    stv = None
    누적수익 = 0

    def __init__(self, _stv = None):
        super(KiwoomTester, self).__init__()
        global log, res, err_log
        log, res, err_log = log_manager.Log().get_logger()
        self.stv = _stv
        self.chart = ctm.Chart_Manger(self.stv)

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())

    def send_order(self):
        pass

    def calc_profit(self):
        pass

    def add_contract(self):
        pass

    def remove_contract(self):
        pass

    def check_contract_in_candle(self, 종목코드, 캔들, 인덱스):
        return stm.check_contract_in_candle(종목코드, 캔들, 인덱스)

