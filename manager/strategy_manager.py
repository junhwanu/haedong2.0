# -*- coding: utf-8 -*-
import subject
import log_manager

import para

log, res, err_log = log_manager.Log().get_logger()

def is_it_ok(subject_code, current_price):
    try:
        if subject.info[subject_code]['전략'] == '파라':
            return para.is_it_ok(subject_code, current_price)
        else:
            err_log.error('%s 종목, 전략 선택 에러' % subject_code)
            return {'신규주문': False}

    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def is_it_sell(subject_code, current_price):
    try:
        if subject.info[subject_code]['전략'] == '파라':
            return para.is_it_sell(subject_code, current_price)
        else:
            err_log.error('%s 종목, 전략 선택 에러' % subject_code)
            return {'신규주문': False}

    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def strategy_selector(subject_code, current_price):
    pass