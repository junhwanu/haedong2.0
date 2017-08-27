# -*- coding: utf-8 -*-

from manager import chart_manager as ctm, strategy_manager as stm
from modules import __module
from var import subject

class KiwoomTester(__module.ModuleClass):
    chart = None
    stv = None
    누적수익 = 0

    def __init__(self, _stv = None):
        super(KiwoomTester, self).__init__()
        self.stv = _stv
        self.chart = ctm.Chart_Manger(self.stv)
        self.stm = stm.StrategyManager(subject.Subject())

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())

    def send_order(self, order_info):
        #   여기서 order_info 정보 확인
        #   계약이 없으면 신규매매, 있으면 청산
        #   해당 함수에서 분기해서 add_contract, remove_contract 호출
        #   누적 수익은 remove_contract에서 계산

        pass

    def calc_profit(self):
        pass

    def add_contract(self):
        pass

    def remove_contract(self):
        pass

    def check_contract_in_candle(self, 종목코드, 캔들, 인덱스):
        return stm.check_contract_in_candle(종목코드, 캔들, 인덱스)

