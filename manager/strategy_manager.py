# -*- coding: utf-8 -*-
import subject
import log_manager

import para
from constant import *
import configparser
import strategy_var as st
import json

log, res, err_log = log_manager.Log().get_logger()

def is_it_ok(subject_code, current_price):
    try:
        if subject.info[subject_code]['전략'] == 파라:
            return para.is_it_ok(subject_code, current_price)
        else:
            err_log.error('%s 종목, 전략 선택 에러' % subject_code)
            return {'신규주문': False}

    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def is_it_sell(subject_code, current_price):
    try:
        if subject.info[subject_code]['전략'] == 파라:
            return para.is_it_sell(subject_code, current_price)
        else:
            err_log.error('%s 종목, 전략 선택 에러' % subject_code)
            return {'신규주문': False}

    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def strategy_selector(subject_code, current_price):
    pass

def set_strategy_var(stv):
    try:
        # 전략 변수 Config 불러오기
        config = configparser.RawConfigParser()
        config.read(CONFIG_PATH + '/strategy_var.cfg')

        for subject_code in subject.info.keys():
            subject_symbol = subject_code[:2]

            if subject_symbol not in stv.info:
                stv.info[subject_symbol] = {}

            strategy = config.get(ST_CONFIG, subject_symbol)
            stv.info[subject_symbol][strategy] = {}

            stv.info[subject_symbol][strategy][차트] = []
            stv.info[subject_symbol][strategy][차트변수] = {}
            stv.info[subject_symbol][strategy][차트변수][틱차트] = {}
            stv.info[subject_symbol][strategy][차트변수][분차트] = {}

            if strategy == 파라:
                stv.info[subject_symbol][strategy][차트변수][매매불가수익량] = config.get(subject_symbol, 매매불가수익량)
                stv.info[subject_symbol][strategy][차트변수][청산단계별드리블틱] = json.loads(config.get(subject_symbol, 청산단계별드리블틱))

            ## subject_symbol의 config 불러옴
            chart_types = json.loads(config.get(subject_symbol, CHART_TYPE))

            for chart_type in chart_types:
                type = chart_type.split('_')[0]
                time_unit = chart_type.split('_')[1]

                section_str = subject_symbol + '_' + chart_type
                stv.info[subject_symbol][strategy][차트변수][type][time_unit] = {}
                stv.info[subject_symbol][strategy][차트].append( [ str(type), str(time_unit) ] )
                if strategy == 파라:
                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][이동평균선] = json.loads(config.get(section_str, 이동평균선))
                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][INIT_AF] = config.getfloat(section_str, INIT_AF)
                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][MAX_AF] = config.getfloat(section_str, MAX_AF)
                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][초기캔들수] = config.getint(section_str, 초기캔들수)


    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))