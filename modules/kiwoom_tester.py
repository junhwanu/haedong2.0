# -*- coding: utf-8 -*-

from constant import const
from manager import chart_manager as ctm, strategy_manager as stm, contract_manager as cm
from modules import __module
from var import subject


class KiwoomTester(__module.ModuleClass):
    chart = None
    stv = None

    누적수익 = 0

    def __init__(self, stv, common_data):
        super(KiwoomTester, self).__init__()
        self.stv = stv
        self.sbv = subject.Subject()
        self.chart = ctm.ChartManger(self.stv, self.sbv)
        self.stm = stm.StrategyManager(self.stv, self.sbv, self.chart)

        self.cm = cm.ContractManager()

        for subject_code in common_data.keys():
            self.chart.init_data(subject_code, common_data)


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
#         from math import floor
        차트 = self.chart.data[종목코드][차트타입][시간단위]

        if 인덱스 < 500: return const.false

        sar = 차트['SAR'][-1]
        플로우 = 차트['플로우'][-1]
        자릿수 = self.sbv.info[종목코드]['자릿수'] # 금의 경우 1
        단위 = self.sbv.info[종목코드]['단위']     # 금의 경우 0.1

#         self.log.info("인덱스 : %s, SARz : %s" % (인덱스, sar))

        if self.cm.get_contract_count(종목코드) > 0: #계약을 가지고 있을때
            if 플로우 == const.상향:
                if 차트[const.저가][인덱스] < sar: # 하향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_sell(종목코드, round(sar-(단위/2),자릿수))
            elif 플로우 == const.하향:
                if 차트[const.고가][인덱스] >= sar: # 상향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_sell(종목코드, round(sar-(단위/2),자릿수) + 단위)
        else: # 계약을 가지고 있지 않을 때
            if 플로우 == const.상향:
                if 차트[const.저가][인덱스] < sar: # 하향 반전 됨
                    return self.stm.get_strategy(종목코드).is_it_ok(종목코드, round(sar-(단위/2),자릿수))

            elif 플로우 == const.하향:
                if 차트[const.고가][인덱스] >= sar:
                    return self.stm.get_strategy(종목코드).is_it_ok(종목코드, round(sar-(단위/2),자릿수) + 단위)



    def run(self, subject_code, chart_type, time_unit):
        self.log.info(self.chart.data)

        #try:
        # 이후 여러종목 동시테스트일 경우에는 캔들의 시간이 빠른순으로 넣어줘야함. 같은 종목도 차트타입과 시간단위도 마찬가지로 차트가 여러개일 경우엔
        for i in range(0, len(self.chart.data[subject_code][chart_type][time_unit][const.현재가])):
            self.check_contract_in_candle(subject_code, chart_type, time_unit, i)
            self.chart.data[subject_code][chart_type][time_unit]['인덱스'] += 1
            self.chart.calc(subject_code, chart_type, time_unit)
        #except Exception as err:
        #    self.log.error(err)