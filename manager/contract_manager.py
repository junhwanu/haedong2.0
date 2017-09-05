# -*- coding: utf-8 -*-
from constant import constant_ as const
# from strategy import para
from utils import util
from var import subject
from manager.__manager import ManagerClass


SAFE = '목표달성청산'
DRIBBLE = '드리블'
ALL = '전체'


class ContractManager(ManagerClass):
    contract_list = {}

    '''
    싹 바꿔야함 contract 클래스 따로따로 관리말고,
    키움에서 2개 매도 후 한참뒤에 1개 매도하면 합쳐져서 3개로 관리하므로
    우리도 평균가로 합쳐서 관리해야함
    합친 평균 체결가 구하는 방법을 알아내서 체결표시가 바꿔서 넣어야함
    '''

    def __init__(self):
        super(ContractManager, self).__init__()
        self.sbv = subject.Subject()

    def add_contract(self, order_info):
        try:
            subject_code = order_info['종목코드']

            if subject_code in self.contract_list:  # 가지고 있는 계약이면
                c = self.contract_list[subject_code]

                self.log.info('%s 종목은 이미 %s계약 보유 중 입니다' % (subject_code, self.contract_list[subject_code]['보유수량']))
                self.log.info('%s 종목 신규 계약 %d개 추가 합니다.' % (subject_code, int(order_info['신규수량'])))

                # 정확한 체결가를 위해 체결가 다시 계산
                c['체결가'] = ((c['체결가'] * c['보유수량']) + (order_info['체결표시가격']\
                    * int(order_info['신규수량']))) / (c['보유수량'] + int(order_info['신규수량']))
                c['체결가'] = round(float(order_info['체결표시가격']), self.sbv.info[order_info['종목코드']]['자릿수'])

                if self.sbv.info[subject_code]['상태'] == '매매시도중' or self.sbv.info[subject_code]['상태'] == '매수중' \
                        or self.sbv.info[subject_code]['상태'] == '매도중':

                    if c['계약타입'][SAFE] > c['계약타입'][DRIBBLE]:
                        safe_num = int(int(order_info['신규수량']) / 2)
                        dribble_num = int(order_info['신규수량']) - safe_num
                    else:
                        dribble_num = int(int(order_info['신규수량']) / 2)
                        safe_num = int(order_info['신규수량']) - dribble_num

                    c['계약타입'][SAFE] += safe_num
                    c['계약타입'][DRIBBLE] += dribble_num

                    c['보유수량'] = c['보유수량'] + safe_num + dribble_num

                    self.log.info('종목코드 : ' + subject_code + ', 목표달성청산수량 ' + str(safe_num) + '개, 드리블수량 ' + str(
                        dribble_num) + '개 추가.')
                else:
                    self.err_log.log("%s 상태 이상으로 계약 추가를 수행하지 못하였습니다." % subject_code)

            else:  # 신규 계약 이면
                self.log.info("%s 신규 계약 추가: %s" % (subject_code, order_info))
                self.contract_list[subject_code] = {}
                c = self.contract_list[subject_code]

                safe_num = int(int(order_info['신규수량']) / 2)
                dribble_num = int(order_info['신규수량']) - safe_num

                c['보유수량'] = int(order_info['신규수량'])
                c['계약타입'] = {}
                c['계약타입'][SAFE] = safe_num
                c['계약타입'][DRIBBLE] = dribble_num
                c['체결가'] = float(order_info['체결표시가격'])
                c['매도수구분'] = order_info['매도수구분']
                c['전략'] = self.sbv.info[subject_code]['전략']

                if self.sbv.info[subject_code]['전략'] == '파라':

                    order_info['익절틱'], order_info['손절틱'] = self.get_loss_cut(self.sbv.info[subject_code]['전략'])
                    c['익절가'] = []
                    c['손절가'] = []

                    if order_info['매도수구분'] == const.매도:
                        for i in range(len(order_info['익절틱'])):
                            c['익절가'].append(c['체결가'] - order_info['익절틱'][i] * self.sbv.info[subject_code]['단위'])
                        for i in range(len(order_info['손절틱'])):
                            c['손절가'].append(c['체결가'] + order_info['손절틱'][i] * self.sbv.info[subject_code]['단위'])

                    elif order_info['매도수구분'] == const.매수:
                        for i in range(len(order_info['익절틱'])):
                            c['익절가'] = c['체결가'] + order_info['익절틱'][i] * \
                                                  self.sbv.info[subject_code]['단위']
                        for i in range(len(order_info['손절틱'])):
                            c['손절가'] = c['체결가'] - order_info['손절틱'][i] * \
                                                  self.sbv.info[subject_code]['단위']

                    self.log.info('신규계약 추가, 종목코드 : ' + subject_code + ', 목표달성청산수량 ' + str(safe_num) + '개, 드리블수량 ' + str(
                        dribble_num) + '개 추가.')

        except Exception as err:
            self.err_log.error(util.get_error_msg(err))

    def remove_contract(self, order_info):
        try:
            profit = 0
            remove_cnt = order_info['청산수량']
            subject_code = order_info['종목코드']

            c = self.contract_list[subject_code]
            if c['보유수량'] >= remove_cnt:
                c['보유수량'] -= remove_cnt
                if c['계약타입'][SAFE] > 0:
                    # c['계약타입'][SAFE] - remove_cnt
                    remove_cnt -= c['계약타입'][SAFE]
                    if remove_cnt > 0:
                        c['계약타입'][DRIBBLE] -= remove_cnt

                if c['보유수량'] <= 0:
                    c['보유수량'] = 0
                    c['계약타입'][SAFE] = 0
                    c['계약타입'][DRIBBLE] = 0

            else:
                self.err_log.info("보유 수량보다 많은 수의 계약을 삭제할수 없습니다.")
                remove_cnt -= c['보유수량']
                c['보유수량'] = 0
                c['계약타입'][SAFE] = 0
                c['계약타입'][DRIBBLE] = 0

            c['체결가'] = round(float(order_info['체결표시가격']), self.sbv.info[order_info['종목코드']]['자릿수'])
            if order_info['매도수구분'] == const.매수:
                profit = (remove_cnt * (c['체결가'] - order_info['체결표시가격'])) * self.sbv.info[subject_code]['틱가치']
            elif order_info['매도수구분'] == const.매도:
                profit = (remove_cnt * (order_info['체결표시가격'] - c.체결표시가격)) * self.sbv.info[subject_code]['틱가치']

            return profit
        except Exception as err:
            self.err_log.error(util.get_error_msg(err))

    @staticmethod
    def get_contract_count(self, subject_code):
        try:
            if subject_code not in self.contract_list:
                return 0
            return self.contract_list[subject_code]['보유수량']
        except Exception as err:
            self.err_log.error(util.get_error_msg(err))
            return 0

    def get_contract_list(self, subject_code):
        if subject_code not in self.contract_list:
            return []

        return self.contract_list[subject_code]

    @staticmethod
    def get_loss_cut(strategy):
        # return [익절가], [손절가]
        if strategy == const.파라:
            return [const.INFINITY, 77, 300], [50, const.ZERO, const.ZERO]

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())

