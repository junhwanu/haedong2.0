# -*- coding: utf-8 -*-
import subject
import log_manager

import para

log, res, err = log_manager.Log().get_logger()

def is_it_ok(subject_code, current_price):
    if subject.info[subject_code]['전략'] == '파라':
        return para.is_it_ok(subject_code, current_price)
    else:
        err.info('%s 종목, 전략 선택 에러' % subject_code)
        return {'신규주문': False}

def is_it_sell(subject_code, current_price):
    if subject.info[subject_code]['전략'] == '파라':
        return para.is_it_sell(subject_code, current_price)
    else:
        err.info('%s 종목, 전략 선택 에러' % subject_code)
        return {'신규주문': False}

def strategy_selector(subject_code, current_price):
    pass