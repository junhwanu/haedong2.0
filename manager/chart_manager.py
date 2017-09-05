# -*- coding: utf-8 -*-
import time

from constant import constant_ as const
# from var import subject, strategy_var as st
from utils import util
from manager.__manager import ManagerClass


class ChartManger(ManagerClass):
    common_data = {}
    
    data = {}
    stv = None

    running_time = 0

#     def __init__(self):
#         super(ChartManger, self).__init__()

    def __init__(self, stv, sbv):
        super(ChartManger, self).__init__()
        self.stv = stv
        self.sbv = sbv

    def init_data(self, subject_code):
        try:
            s_time = time.time()

            self.data[subject_code] = {}
            self.data[subject_code]['상태'] = '대기'

            if self.sbv.info[subject_code]['전략'] == const.파라:
                for chart_config in self.stv.info[subject_code][const.파라][const.차트]:
                    chart_type = chart_config[0]
                    time_unit = chart_config[1]

                    if chart_type == const.틱차트:
                        if const.틱차트 not in self.data[subject_code]:
                            self.data[subject_code][chart_type] = {}

                        self.data[subject_code][chart_type][time_unit] = {}

                        if const.MODE == const.REAL:
                            self.data[subject_code][chart_type][time_unit][const.현재가] = []
                            self.data[subject_code][chart_type][time_unit][const.시가] = []
                            self.data[subject_code][chart_type][time_unit][const.고가] = []
                            self.data[subject_code][chart_type][time_unit][const.저가] = []
                            self.data[subject_code][chart_type][time_unit][const.체결시간] = []
                            self.data[subject_code][chart_type][time_unit]['영업일자'] = []
                            self.data[subject_code][chart_type][time_unit]['거래량'] = []
                            self.data[subject_code][chart_type][time_unit]['인덱스'] = -1
                        elif const.MODE == const.TEST:
                            self.data[subject_code][chart_type][time_unit] = common_data[subject_code][chart_type][time_unit]
                            self.data[subject_code][chart_type][time_unit]['인덱스'] = 0

                        self.data[subject_code][chart_type][time_unit]['현재가변동횟수'] = 0
                        self.data[subject_code][chart_type][time_unit]['현재캔들'] = {}
                        self.data[subject_code][chart_type][time_unit]['임시캔들'] = []
                        self.data[subject_code][chart_type][time_unit]['임시데이터'] = []
                        self.data[subject_code][chart_type][time_unit]['임시틱'] = []
                        self.data[subject_code][chart_type][time_unit]['차트타입'] = chart_type
                        self.data[subject_code][chart_type][time_unit]['시간단위'] = time_unit

                        self.data[subject_code][chart_type][time_unit][const.이동평균선] = {}
                        self.data[subject_code][chart_type][time_unit][const.이동평균선]['일수'] = self.stv.info[subject_code][self.sbv.info[subject_code]['전략']][const.차트변수][chart_type][time_unit][const.이동평균선]
                        self.data[subject_code][chart_type][time_unit]['지수이동평균선'] = {}

                        for days in self.data[subject_code][chart_type][time_unit][const.이동평균선]['일수']:
                            self.data[subject_code][chart_type][time_unit][const.이동평균선][days] = []
                            self.data[subject_code][chart_type][time_unit]['지수이동평균선'][days] = []

                        self.data[subject_code][chart_type][time_unit]['볼린저밴드'] = {}
                        self.data[subject_code][chart_type][time_unit]['볼린저밴드']['중심선'] = []
                        self.data[subject_code][chart_type][time_unit]['볼린저밴드']['상한선'] = []
                        self.data[subject_code][chart_type][time_unit]['볼린저밴드']['하한선'] = []
                        self.data[subject_code][chart_type][time_unit]['볼린저밴드']['캔들위치'] = []

                        self.data[subject_code][chart_type][time_unit]['일목균형표'] = {}
                        self.data[subject_code][chart_type][time_unit]['일목균형표']['전환선'] = []
                        self.data[subject_code][chart_type][time_unit]['일목균형표']['기준선'] = []
                        self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'] = []
                        self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'] = []
                        for index in range(0, 26):
                            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)
                            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)

                        self.data[subject_code][chart_type][time_unit]['현재SAR'] = 0  # 현재 SAR
                        self.data[subject_code][chart_type][time_unit]['SAR'] = []
                        self.data[subject_code][chart_type][time_unit]['EP'] = 0
                        self.data[subject_code][chart_type][time_unit]['AF'] = 0
                        self.data[subject_code][chart_type][time_unit]['현재플로우'] = ''
                        self.data[subject_code][chart_type][time_unit]['플로우'] = []
                        self.data[subject_code][chart_type][time_unit]['지난플로우'] = []  # [ {'추세': '상향', '시작SAR': 1209.3 '마지막SAR': 1212.4 }, {'추세': '하향', '시작SAR': 1212.4 '마지막SAR': 1211.0 } ]
                    elif chart_type is const.분차트:
                        self.data[subject_code][chart_type][time_unit]['현재가변동시간'] = []
                        pass

            else:
                '''
                self.data[subject_code][chart_type][time_unit]['일목균형표'] = {}
                self.data[subject_code][chart_type][time_unit]['일목균형표']['전환선'] = []
                self.data[subject_code][chart_type][time_unit]['일목균형표']['기준선'] = []
                self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'] = []
                self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'] = []
                for index in range(0, 26):
                    self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)
                    self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)
                '''

            self.running_time = self.running_time + (time.time() - s_time)

        except Exception as err:
            self.log.error(util.get_error_msg(err))

    def clear_data(self, subject_code):
        del self.data[subject_code]

    def init_current_candle(self, subject_code, chart_type, time_unit):
        s_time = time.time()
        self.data[subject_code][chart_type][time_unit]['현재캔들'][const.고가] = 0
        self.data[subject_code][chart_type][time_unit]['현재캔들'][const.저가] = const.INFINITY

        if chart_type is const.틱차트:
            self.data[subject_code][chart_type][time_unit]['현재가변동횟수'] = 0
        elif chart_type is const.분차트:
            self.data[subject_code][chart_type][time_unit]['현재가변동시간'] = '?????'

        self.running_time = self.running_time + (time.time() - s_time)

    def push(self, subject_code, chart_type, time_unit, candle):
        try:
            s_time = time.time()

            self.data[subject_code][chart_type][time_unit][const.현재가].append(candle[const.현재가])
            self.data[subject_code][chart_type][time_unit][const.시가].append(candle[const.시가])
            self.data[subject_code][chart_type][time_unit][const.고가].append(candle[const.고가])
            self.data[subject_code][chart_type][time_unit][const.저가].append(candle[const.저가])
            self.data[subject_code][chart_type][time_unit][const.체결시간].append(candle[const.체결시간])
            if '영업일자' in candle: self.data[subject_code][chart_type][time_unit]['영업일자'].append(candle['영업일자'])
            if '거래량' in candle: self.data[subject_code][chart_type][time_unit]['거래량'].append(candle['거래량'])
            self.data[subject_code][chart_type][time_unit]['인덱스'] += 1

            self.calc(subject_code, chart_type, time_unit)

            self.running_time = self.running_time + (time.time() - s_time)

        except Exception as err:
            self.log.error(util.get_error_msg(err))

    def calc_common_data(self, subject_code, chart_type, time_unit):
        for idx in range(0, len(self.data[subject_code][chart_type][time_unit])):
            pass
        pass

    def calc(self, subject_code, chart_type, time_unit):
        try:
            if self.sbv.info[subject_code]['전략'] == const.파라:
                self.calc_ma_line(subject_code, chart_type, time_unit)
                #calc_ema_line(subject_code, chart_type, time_unit)
                #calc_ilmok_chart(subject_code, chart_type, time_unit)

                if self.data[subject_code][chart_type][time_unit]['인덱스'] < 5:
                    self.data[subject_code][chart_type][time_unit]['플로우'].append('모름')
                    self.data[subject_code][chart_type][time_unit]['SAR'].append(0)
                elif self.data[subject_code][chart_type][time_unit]['인덱스'] == 5:
                    self.init_sar(subject_code, chart_type, time_unit)
                else:
                    self.calc_sar(subject_code, chart_type, time_unit)

        except Exception as err:
            self.log.error(util.get_error_msg(err))

    def calc_ma_line(self, subject_code, chart_type, time_unit):
        '''
        이동평균선 계산
        '''
        for days in self.data[subject_code][chart_type][time_unit][const.이동평균선]['일수']:
            if self.data[subject_code][chart_type][time_unit]['인덱스'] >= days - 1:
                avg = sum(
                    self.data[subject_code][chart_type][time_unit][const.현재가][
                    self.data[subject_code][chart_type][time_unit]['인덱스'] - days + 1: self.data[subject_code][chart_type][time_unit][
                                                                                     '인덱스'] + 1]) / days
                self.data[subject_code][chart_type][time_unit][const.이동평균선][days].append(avg)
            else:
                self.data[subject_code][chart_type][time_unit][const.이동평균선][days].append(None)

    def calc_ema_line(self, subject_code, chart_type, time_unit):
        '''
        지수이동평균선 계산
        '''
        for days in self.data[subject_code][chart_type][time_unit][const.이동평균선]['일수']:
            if self.data[subject_code][chart_type][time_unit]['인덱스'] >= days - 1:
                if self.data[subject_code][chart_type][time_unit]['인덱스'] == days - 1:
                    avg = sum(self.data[subject_code][chart_type][time_unit][const.현재가][
                              self.data[subject_code][chart_type][time_unit]['인덱스'] - days + 1:
                              self.data[subject_code][chart_type][time_unit]['인덱스'] + 1]) / days
                    self.data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(avg)
                else:
                    alpha = 2 / (days + 1)
                    ema = alpha * self.data[subject_code][chart_type][time_unit][const.현재가][-1] + (1.0 - alpha) * \
                                                                                              self.data[subject_code][chart_type][
                                                                                             time_unit]['지수이동평균선'][days][-1]
                    self.data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(ema)
            else:
                self.data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(None)

    def calc_ilmok_chart(self, subject_code, chart_type, time_unit):
        '''
        일목균형표 계산
        '''
        if self.data[subject_code][chart_type][time_unit]['인덱스'] < 9:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['전환선'].append(None)
        else:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['전환선'].append((max(
                self.data[subject_code][chart_type][time_unit][const.현재가][
                    self.data[subject_code][chart_type][time_unit]['인덱스'] - 9: self.data[subject_code][chart_type][time_unit][
                        '인덱스']]) + min(
                            self.data[subject_code][chart_type][time_unit][const.현재가][
                                self.data[subject_code][chart_type][time_unit]['인덱스'] - 9: self.data[subject_code][chart_type][time_unit][
                                    '인덱스']])) / 2)

        if self.data[subject_code][chart_type][time_unit]['인덱스'] < 26:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['기준선'].append(None)
        else:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['기준선'].append((max(
                self.data[subject_code][chart_type][time_unit][const.현재가][
                self.data[subject_code][chart_type][time_unit]['인덱스'] - 26: self.data[subject_code][chart_type][time_unit][
                    '인덱스']]) + min(
                self.data[subject_code][chart_type][time_unit][const.현재가][
                self.data[subject_code][chart_type][time_unit]['인덱스'] - 26: self.data[subject_code][chart_type][time_unit][
                    '인덱스']])) / 2)

        if self.data[subject_code][chart_type][time_unit]['인덱스'] >= 26:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append((self.data[subject_code][chart_type][time_unit][
                                                                                    '일목균형표']['전환선'][
                                                                                         self.data[subject_code][chart_type][
                                                                                        time_unit]['인덱스']] +
                                                                                     self.data[subject_code][chart_type][time_unit][
                                                                                    '일목균형표']['기준선'][
                                                                                         self.data[subject_code][chart_type][
                                                                                        time_unit]['인덱스']]) / 2)
        else:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)

        if self.data[subject_code][chart_type][time_unit]['인덱스'] >= 52:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append((max(
                self.data[subject_code][chart_type][time_unit][const.현재가][
                self.data[subject_code][chart_type][time_unit]['인덱스'] - 52: self.data[subject_code][chart_type][time_unit][
                    '인덱스']]) + min(
                self.data[subject_code][chart_type][time_unit][const.현재가][
                self.data[subject_code][chart_type][time_unit]['인덱스'] - 52: self.data[subject_code][chart_type][time_unit][
                    '인덱스']])) / 2)
        else:
            self.data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)

    def init_sar(self, subject_code, chart_type, time_unit):
        ep = self.data[subject_code][chart_type][time_unit]['EP']
        af = self.stv.info[subject_code][const.파라][const.차트변수][chart_type][time_unit][const.INIT_AF]
        idx = self.data[subject_code][chart_type][time_unit]['인덱스']

        temp_high_price_list = []
        temp_low_price_list = []

        for i in range(idx):
            temp_high_price_list.append(self.data[subject_code][chart_type][time_unit][const.고가][i])
            temp_low_price_list.append(self.data[subject_code][chart_type][time_unit][const.저가][i])

        score = 0

        for i in range(len(temp_high_price_list) - 1):
            if temp_high_price_list[i] < temp_high_price_list[i + 1]:
                score = score + 1
            else:
                score = score - 1

        if score >= 1:
            init_sar = min(temp_low_price_list)
            temp_flow = "상향"
            ep = max(temp_high_price_list)
        if score < 1:
            init_sar = max(temp_high_price_list)
            ep = min(temp_low_price_list)
            temp_flow = "하향"

        sar = ((ep - init_sar) * af) + init_sar

        self.data[subject_code][chart_type][time_unit]['SAR'].append(sar)
        self.data[subject_code][chart_type][time_unit]['현재SAR'] = sar
        self.data[subject_code][chart_type][time_unit]['EP'] = ep
        self.data[subject_code][chart_type][time_unit]['AF'] = af
        self.data[subject_code][chart_type][time_unit]['현재플로우'] = temp_flow
        self.data[subject_code][chart_type][time_unit]['플로우'].append(temp_flow)

        self.calc_sar(subject_code, chart_type, time_unit)

    def calc_sar(self, subject_code, chart_type, time_unit):
        sar = self.data[subject_code][chart_type][time_unit]['SAR'][-1]
        ep = self.data[subject_code][chart_type][time_unit]['EP']
        temp_flow = self.data[subject_code][chart_type][time_unit]['플로우'][-1]
        af = self.data[subject_code][chart_type][time_unit]['AF']
        init_af = self.stv.info[subject_code][const.파라][const.차트변수][chart_type][time_unit][const.INIT_AF]
        max_af = self.stv.info[subject_code][const.파라][const.차트변수][chart_type][time_unit][const.MAX_AF]
        index = self.data[subject_code][chart_type][time_unit]['인덱스']
        temp_sar = sar

        the_highest_price = 0
        the_lowest_price = 0

        if temp_flow == "상향":
            the_highest_price = ep
        if temp_flow == "하향":
            the_lowest_price = ep

        next_sar = temp_sar

        if temp_flow == "상향":
            if self.data[subject_code][chart_type][time_unit][const.저가][index] >= next_sar:  # 상승추세에서 저가가 내일의 SAR보다 높으면 하락이 유효
                today_sar = next_sar
                temp_flow = "상향"
                the_lowest_price = 0
                if self.data[subject_code][chart_type][time_unit][const.고가][index] > ep:  # 신고가 발생
                    the_highest_price = self.data[subject_code][chart_type][time_unit][const.고가][index]
                    ep = self.data[subject_code][chart_type][time_unit][const.고가][index]
                    af = af + init_af
                    if af > max_af:
                        af = max_af

            elif self.data[subject_code][chart_type][time_unit][const.저가][index] < next_sar:  # 상승추세에서 저가가 내일의 SAR보다 낮으면 하향 반전
                temp_flow = "하향"
                af = init_af
                today_sar = ep
                the_highest_price = 0
                the_lowest_price = self.data[subject_code][chart_type][time_unit][const.저가][index]

                ep = the_lowest_price
                self.log.info("%s, %s, %s : 하향 반전, 시간 : %s" % (
                    subject_code, chart_type, time_unit, self.data[subject_code][chart_type][time_unit][const.체결시간][-1]))

                flow_result = {}
                flow_result['추세'] = const.상향
                flow_result['마지막SAR'] = next_sar
                if len(self.data[subject_code][chart_type][time_unit]['지난플로우']) == 0:
                    flow_result['시작SAR'] = 0
                else:
                    flow_result['시작SAR'] = self.data[subject_code][chart_type][time_unit]['지난플로우'][-1]['마지막SAR']

                    self.data[subject_code][chart_type][time_unit]['지난플로우'].append(flow_result)

        elif temp_flow == "하향":
            if self.data[subject_code][chart_type][time_unit][const.고가][index] <= next_sar:  # 하락추세에서 고가가 내일의 SAR보다 낮으면 하락이 유효
                today_sar = next_sar
                temp_flow = "하향"
                the_highest_price = 0
                if self.data[subject_code][chart_type][time_unit][const.저가][index] < ep:  # 신저가 발생
                    the_lowest_price = self.data[subject_code][chart_type][time_unit][const.저가][index]
                    ep = self.data[subject_code][chart_type][time_unit][const.저가][index]
                    af = af + init_af
                    if af > max_af:
                        af = max_af

            elif self.data[subject_code][chart_type][time_unit][const.고가][index] > next_sar:  # 하락추세에서 고가가 내일의 SAR보다 높으면 상향 반전
                temp_flow = "상향"
                af = init_af
                today_sar = ep
                the_lowest_price = 0
                the_highest_price = self.data[subject_code][chart_type][time_unit][const.고가][index]

                ep = the_highest_price
                self.log.info("%s, %s, %s : 상향 반전, 시간 : %s" % (
                    subject_code, chart_type, time_unit, self.data[subject_code][chart_type][time_unit][const.체결시간][-1]))

                flow_result = {}
                flow_result['추세'] = const.하향
                flow_result['마지막SAR'] = next_sar
                if len(self.data[subject_code][chart_type][time_unit]['지난플로우']) == 0:
                    flow_result['시작SAR'] = 0
                else:
                    flow_result['시작SAR'] = self.data[subject_code][chart_type][time_unit]['지난플로우'][-1]['마지막SAR']

                    self.data[subject_code][chart_type][time_unit]['지난플로우'].append(flow_result)

        next_sar = today_sar + af * (max(the_highest_price, the_lowest_price) - today_sar)

        self.data[subject_code][chart_type][time_unit]['SAR'].append(next_sar)
        self.data[subject_code][chart_type][time_unit]['현재SAR'] = next_sar
        self.data[subject_code][chart_type][time_unit]['EP'] = ep
        self.data[subject_code][chart_type][time_unit]['AF'] = af
        self.data[subject_code][chart_type][time_unit]['현재플로우'] = temp_flow
        self.data[subject_code][chart_type][time_unit]['플로우'].append(temp_flow)

    def set_stv(self, stv_):
        self.stv = stv_

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
