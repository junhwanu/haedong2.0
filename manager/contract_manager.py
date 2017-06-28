# -*- coding: utf-8 -*-
from contract import contract
import subject
import log_manager
import para
from constant import *

log, res, err_log = log_manager.Log().get_logger()

예수금 = 0
contract_list = {}

'''

싹 바꿔야함 contract 클래스 따로따로 관리말고,
키움에서 2개 매도 후 한참뒤에 1개 매도하면 합쳐져서 3개로 관리하므로
우리도 평균가로 합쳐서 관리해야함
합친 평균 체결가 구하는 방법을 알아내서 체결표시가 바꿔서 넣어야함


'''
def add_contract(order_info):
    try:
        c = contract_list[order_info['종목코드']]
        if order_info['종목코드'] not in contract_list:
            c = contract(order_info)
        else:
            c.수량 += int(order_info['신규수량'])

            ''' 체결표시가격 기존 가격과 합해서 평균가로 정리해야됨 '''
            c.체결표시가격 = float(order_info['체결표시가격'])
            c.종목코드 = order_info['종목코드']
            c.매도수구분 = order_info['매도수구분']

            if subject.info[c.종목코드]['전략'] == '파라':
                c.익절가, c.손절가 = para.get_loss_cut()
                if c.매도수구분 == 매수:
                    for i in range(len(c.익절가)):
                        c.익절가[i] = c.체결표시가격 + c.익절가[i]
                    for i in range(len(c.손절가)):
                        c.손절가[i] = c.체결표시가격 - c.손절가[i]

                elif c.매도수구분 == 매도:
                    for i in range(len(c.익절가)):
                        c.익절가[i] = c.체결표시가격 - c.익절가[i]
                    for i in range(len(c.손절가)):
                        c.손절가[i] = c.체결표시가격 + c.손절가[i]


    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def remove_contract(order_info):
    try:
        profit = 0
        remove_cnt = order_info['청산수량']
        subject_code = order_info['종목코드']

        c = contract_list[subject_code]
        if c.수량 >= remove_cnt:
            c.수량 -= remove_cnt
        else:
            remove_cnt -= c.수량
            c.수량 = 0

        if order_info['매도수구분'] == 매수:
            profit = (remove_cnt * (c.체결표시가격 - order_info['체결표시가격'])) * subject.info[subject_code]['틱가치']
        elif order_info['매도수구분'] == 매도:
            profit = (remove_cnt * (order_info['체결표시가격'] - c.체결표시가격)) * subject.info[subject_code]['틱가치']

        return profit
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def get_contract_count(subject_code):
    try:
        if subject_code not in contract_list: return 0

        cnt = 0
        for contract in contract_list[subject_code]:
            cnt = cnt + contract.수량
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

        return 0

    return cnt

def get_contract_list(subject_code):
    if subject_code not in contract_list: return []

    return contract_list[subject_code]