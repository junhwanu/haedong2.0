# -*- coding: utf-8 -*-

from manager import chart_manager as ctm, strategy_manager as stm
from modules import __module
from var import subject
from constant import constant as const
from modules.__module import ModuleClass

class KiwoomTester(__module.ModuleClass):
    chart = None
    stv = None
    누적수익 = 0

    def __init__(self, _stv = None):
        super(KiwoomTester, self).__init__()
        self.stv = _stv
        self.chart = ctm.ChartManger(self.stv, subject.Subject())
        self.stm = stm.StrategyManager(subject.Subject())
        self.subject_var = subject.Subject()


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

    def check_contract_in_candle(self, 종목코드, 차트타입, 시간단위, 인덱스):
        from math import floor
        차트 = self.chart.data[종목코드][차트타입][시간단위]

        sar = 차트['SAR'][-1]
        플로우 = 차트['플로우'][-1]
        자릿수 = self.subject_var.info[종목코드]['자릿수'] # 금의 경우 1
        단위 = self.subject_var.info[종목코드]['단위']     # 금의 경우 0.1

        if ctm().get_contract_count(종목코드) > 0: #계약을 가지고 있을때
            if 플로우 == const.상향:
                if 차트[const.저가] < sar: # 하향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_sell(종목코드, round(sar-(단위/2),자릿수))

            elif 플로우 == const.하향:
                if 차트[const.고가] >= sar: # 상향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_sell(종목코드, round(sar-(단위/2),자릿수) + 단위)

        else: # 계약을 가지고 있지 않을 때
            if 플로우 == const.상향:
                if 차트[const.저가] < sar: # 하향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_ok(종목코드, round(sar-(단위/2),자릿수))

            elif 플로우 == const.하향:
                if 차트[const.고가] >= sar:
                    return self.stm.get_strategy(종목코드).is_it_ok(종목코드, round(sar-(단위/2),자릿수) + 단위)
        pass