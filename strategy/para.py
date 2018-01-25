# -*- coding: utf-8 -*-

import time

from constant import const
from strategy import __base_strategy 
from utils import util


class Para(__base_strategy.BaseStrategy):
# class Para():
    running_time = 0
    
    def __init__(self, stv, sbv, chart):
        self.stv = stv
        self.sbv = sbv
        self.chart = chart
#         print(self.stv.info)
#         print(self.sbv)
#         print(self.chart)
        

    
    def is_it_ok(self, subject_code, current_price):
        s_time = time.time()
        #try:
        temp_chart = self.get_chart(subject_code) # 이거 왜 쓴거임?

        ''' 차트 미생성 '''
        for chart_config in self.stv.info[subject_code][const.파라][const.차트]:
            chart_type = chart_config[0]
            time_unit = chart_config[1]

            if self.chart.data[subject_code][chart_type][time_unit]['인덱스'] < self.stv.info[subject_code][const.파라][const.차트변수][chart_type][time_unit][const.초기캔들수]:
                self.running_time = self.running_time + (time.time() - s_time)
                return const.false


        ''' 매매 불가 상태'''
        if self.chart.data[subject_code]['상태'] == '매수중' or self.chart.data[subject_code]['상태'] == '매도중' \
                or self.chart.data[subject_code]['상태'] == '매매시도중' or self.chart.data[subject_code]['상태'] == '청산시도중':
            self.running_time = self.running_time + (time.time() - s_time)
            return const.false

        매도수구분 = self.get_mesu_medo_type(subject_code, current_price, temp_chart[0])

        if not (매도수구분 == const.매수 or 매도수구분 == const.매도):
            self.running_time = self.running_time + (time.time() - s_time)
            return const.false

        ''' 매매 가능으로 변경 '''
        #if chart.data[subject_code]['상태'] == '대기':  chart.data[subject_code]['상태'] = '매매가능'

        ''' 매매 불가 시간 '''
        if 2100 < util.get_time(0,subject_code) < 2230:
            self.running_time = self.running_time + (time.time() - s_time)
            return const.false

        수량 = self.get_buy_count(subject_code, current_price)

        order_contents = {'신규주문': True, '매도수구분': 매도수구분, '수량': 수량}

        self.running_time = self.running_time + (time.time() - s_time)
        return order_contents
        #except Exception as err:
        #    self.err_log.error(util.get_error_msg(err))
    
        #running_time = running_time + (time.time() - s_time)
        #return const.false

    def is_it_sell(self, cm, subject_code, current_price):
        s_time = time.time()
        try:
            if not (self.chart.data[subject_code]['상태'] == '매수중' or self.chart.data[subject_code]['상태'] == '매도중') :
                self.running_time = self.running_time + (time.time() - s_time)
                return const.false
            
            차트 = self.get_chart(self.chart, subject_code)
            계약 = cm.get_contract_list(subject_code)
            #매도수구분 = const.매매없음
            수량 = 0
            보유수량 = cm.get_contract_count(subject_code)
            차트변수 = self.stv.info[subject_code][const.파라]['차트변수']
    
            ''' 반전시 청산 '''
            if 계약.매도수구분 == const.매수:
                if current_price < 차트[0][const.현재SAR]:
                    매도수구분 = const.매도
                    수량 = 보유수량
                    차트[0]['현재플로우'] = const.하향 # 플로우 즉시 반영
                    차트[0][const.현재SAR] = const.ZERO   # 다음 캔들이되어 SAR이 계산되기 전에 새로운 매매가 들어가는 것을 방지
    
            elif 계약.매도수구분 == const.매도:
                if current_price > 차트[0][const.현재SAR]:
                    매도수구분 = const.매수
                    수량 = 보유수량
                    차트[0]['현재플로우'] = const.상향 # 플로우 즉시 반영
                    차트[0][const.현재SAR] = const.INFINITY   # 다음 캔들이되어 SAR이 계산되기 전에 새로운 매매가 들어가는 것을 방지
    
            ''' 손절가 및 청산가에 청산 '''
            if 계약.매도수구분 == const.매수:
                for 청산단계 in range(len(계약.손절가)):
                    손절가 = 계약.손절가[청산단계]
                    if current_price <= 손절가:
                        매도수구분 = const.매도
    
                        if 청산단계 == 0:   # 손절가, 전체 청산
                            수량 = 보유수량
                        elif 청산단계 > 0 and 보유수량 >= 2: # n차청산
                            if 청산단계 == 1:
                                수량 = 보유수량 / 2
                            elif 청산단계 == 2:
                                수량 = (보유수량 + 1) / 2
                            else: 수량 = 보유수량
    
                for 청산단계 in range(len(계약.익절가)):
                    익절가 = 계약.익절가[청산단계]
                    if current_price >= 익절가:
                        if 청산단계 == 0:   # 익절가, 전체 청산
                            매도수구분 = const.매도
                            수량 = 보유수량
                        elif 청산단계 > 0 and 보유수량 >= 2: # n차청산
                            계약.익절가[청산단계] = 계약.익절가[청산단계] + 차트변수[const.청산단계별드리블틱][청산단계]
                            계약.손절가[청산단계] = 계약.손절가[청산단계] + 차트변수[const.청산단계별드리블틱][청산단계]
    
            elif 계약.매도수구분 == const.매도:
                for 청산단계 in range(len(계약.손절가)):
                    손절가 = 계약.손절가[청산단계]
                    if current_price >= 손절가:
                        매도수구분 = const.매도
    
                        if 청산단계 == 0:   # 손절가, 전체 청산
                            수량 = 보유수량
                        elif 청산단계 > 0 and 보유수량 >= 2: # n차청산
                            if 청산단계 == 1:
                                수량 = 보유수량 / 2
                            elif 청산단계 == 2:
                                수량 = (보유수량 + 1) / 2
                            else:
                                수량 = 보유수량
    
                for 청산단계 in range(len(계약.익절가)):
                    익절가 = 계약.익절가[청산단계]
                    if current_price <= 익절가:
                        if 청산단계 == 0:   # 익절가, 전체 청산
                            매도수구분 = const.매도
                            수량 = 보유수량
                        elif 청산단계 > 0 and 보유수량 >= 2: # n차청산
                            계약.익절가[청산단계] = 계약.익절가[청산단계] - 차트변수[const.청산단계별드리블틱][청산단계]
                            계약.손절가[청산단계] = 계약.손절가[청산단계] - 차트변수[const.청산단계별드리블틱][청산단계]
    
            수량 = int(수량)
            if 수량 is 0: return const.false
            order_info = {'신규주문':True, '매도수구분':매도수구분, '수량':수량}
    
            self.running_time = self.running_time + (time.time() - s_time)
            return order_info
        except Exception as err:
            self.err_log.error(util.get_error_msg(err))
    
            self.running_time = self.running_time + (time.time() - s_time)
            return const.false

    def get_chart(self, subject_code):
        temp_chart = []
#         print(self.stv.info)
        for 차트변수 in self.stv.info[subject_code][const.파라][const.차트]:
            temp_chart.append(self.chart.data[subject_code][차트변수[0]][차트변수[1]])
        return temp_chart

    def get_mesu_medo_type(self, subject_code, 현재가, 차트):
        try:
            차트변수 = self.stv.info[subject_code][const.파라]['차트변수']
            차트타입 = 차트['차트타입']
            시간단위 = 차트['시간단위']
            매도수구분 = const.매매없음
            현재플로우 = 차트['현재플로우']
            지난플로우 = 차트['지난플로우'][-5:]
    
            i = 차트['인덱스']

            if (현재플로우 == const.상향 and 차트['플로우'][-1] != 차트['플로우'][-2]) or \
                    (현재플로우 == const.하향 and 현재가 > 차트[const.현재SAR]):
                매도수구분 = const.매수
                차트['현재플로우'] = const.상향  # 현재 플로우 즉시 반영
                차트[const.현재SAR] = const.ZERO
    
            elif (현재플로우 == const.하향 and 차트['플로우'][-1] != 차트['플로우'][-2]) or \
                    (현재플로우 == const.상향 and 현재가 < 차트[const.현재SAR]):
                매도수구분 = const.매도
                차트['현재플로우'] = const.하향  # 현재 플로우 즉시 반영
                차트[const.현재SAR] = const.INFINITY
    
    
            ''' 반전시 매매'''
            if (차트['현재플로우'] == const.상향 and util.is_sorted(subject_code, 차트타입, 시간단위) != const.상승세) or \
                    (차트['현재플로우'] == const.하향 and util.is_sorted(subject_code, 차트타입, 시간단위) != const.하락세):
                ''' 이동평균선 안맞을 시 매매 안함 '''
                self.log.debug('이동평균선 방향이 현재 플로우와 맞지 않아 매매 안함.')
                return const.매매없음
    
            ''' 이전 플로우 수익이 매매불가수익량 이상일 때 매매 안함 '''
            if (지난플로우[0][const.추세] == const.상향 and (지난플로우[0][const.마지막SAR] - 지난플로우[0][const.시작SAR])*self.sbv.info[subject_code]['틱가치'] >= 차트변수[const.매매불가수익량]) or \
                (지난플로우[0][const.추세] == const.하향 and (지난플로우[0][const.시작SAR] - 지난플로우[0][const.마지막SAR])*self.sbv.info[subject_code]['틱가치'] >= 차트변수[const.매매불가수익량]):
                self.log.debug("이전 플로우 수익이 %s틱 이상이므로 현재 플로우는 넘어갑니다." % 차트변수[const.매매불가수익량])
                return const.false
    
            ''' 틀, 틀, 틀, 틀 이후 매매 안함 '''
            맞틀리스트 = []
            for 플로우 in 지난플로우:
                if (플로우[const.추세] == const.상향 and (플로우[const.마지막SAR] - 플로우[const.시작SAR]) > 0) or \
                        (플로우[const.추세] == const.하향 and (플로우[const.마지막SAR] - 플로우[const.시작SAR]) < 0):
                    맞틀리스트.append(const.맞)
                else:
                    맞틀리스트.append(const.틀)
    
    
            if 차트['현재플로우'] != 차트['플로우']:
                ''' 반전되었으나, 캔들이 완성되지 않아 아직 SAR 계산은 이루어지지 않음 '''
                if (차트['플로우'][-1] == const.상향 and (현재가 - 차트['SAR'][-1]) > 0) \
                    or (차트['플로우'][-1] == const.하향 and (현재가 - 차트['SAR'][-1]) < 0):
                    맞틀리스트.append(const.맞)
                else: 맞틀리스트.append(const.틀)
    
            if 맞틀리스트[-5:] == [const.틀, const.틀, const.틀, const.틀, const.틀]:
                self.log.debug("틀 5회 연속으로 매매 안함.")
                return const.false
            elif 맞틀리스트[-4:] == [const.맞, const.틀, const.틀, const.틀]:
                self.log.debug("[맞, 틀, 틀, 틀]로 매매 안함.")
                return const.false
            elif 맞틀리스트[-3:] == [const.맞, const.틀, const.틀]:
                self.log.debug("[맞, 틀, 틀]로 매매 안함.")
                return const.false
            return 매도수구분
    
        except Exception as err:
            self.err_log.error(util.get_error_msg(err))
            return const.매매없음

    def get_buy_count(self, subject_code, current_price):
        return 2

    def get_loss_cut(self, cm, subject_code, current_price):
        ''' return [익절가], [손절가] '''
        if cm.get_contract_list(subject_code) == 1:
            return [const.INFINITY], [50]
        elif cm.get_contract_count(subject_code) >= 2:
            return [const.INFINITY, 77, 300], [50, const.ZERO, const.ZERO]

    def check_contract_in_candle(self, candle, index):
        # TODO
        pass

    def check_contract_in_tick(self, current_price):
        # TODO
        pass

    def set_strategy_var(self):
        # TODO
        pass