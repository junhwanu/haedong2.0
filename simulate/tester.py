# -*- coding: utf-8 -*-
import subject
import time
import strategy_var as st
import kiwoom
import constant as const
from db_manager import *
import log_manager
import chart_manager as chart

log, res, err_log = log_manager.Log().get_logger()
running_time = 0

def proc():
    global running_time
    subject_symbol = ''
    start_date = ''
    end_date = ''
    log.info('종목코드를 입력하세요. [ ex) GC ]')
    subject_symbol = input()

    if subject_symbol not in subject.info:
        log.info('잘못된 종목코드입니다.')
        proc()
        return

    log.info('시작일을 입력하세요.')
    start_date = input()
    if len(start_date) != 8:
        log.info('잘못된 시작일입니다.')
        proc()
        return

    log.info('종료일을 입력하세요.')
    end_date = input()
    if len(end_date) != 8:
        log.info('잘못된 종료일입니다.')
        proc()
        return

    try:
        ''' 해당 종목 테이블 가져옴 '''
        tables = get_table_list(subject_symbol, start_date, end_date)
        table_list = {}
        subject_codes = []
        for table in tables:
            table_name = table[0]
            subject_code = table_name[: len(subject_symbol) + 3]
            if subject_code not in table_list:
                table_list[subject_code] = []
                subject_codes.append(subject_code)
                subject.info[subject_code] = subject.info[subject_symbol]   # 종목정보 복사
                st.info[subject_code] = st.info[subject_symbol] # 전략변수 복사

            table_list[subject_code].append(table_name)

        ''' 월물별 테이블에서 데이터 가져옴 '''
        data = {}
        for subject_code in subject_codes:
            data[subject_code] = []
            log.info('%s 월물 테이블 내용 수신 시작.' % subject_code)
            for table_name in table_list[subject_code]:
                data[subject_code].append(get_table(table_name))

        test_count = get_simulate_count(subject_symbol) # 총 테스트 횟수 계산

        s_time = time.time()
        for idx in range(test_count):
            for subject_code in subject_codes:
                ''' 전략변수 설정 '''
                set_simulate_config(subject_code)

                kw = kiwoom.Api()

                log.info('%s 월물 테스트 시작.' % subject_code)
                log.info('기간 : %s ~ %s' % (table_list[subject_code][0], table_list[subject_code][-1]))

                chart.init_data(subject_code)
                for chart_config in st.info[subject_code][subject.info[subject_code]['전략']][const.차트]:
                    chart_type = chart_config[0]
                    time_unit = chart_config[1]
                    chart.init_current_candle(subject_code, chart_type, time_unit)  # kiwoom.onReceiveRealData에서 len('현재캔들') == 0이면 캔들을 생성 안하므로 하나 추가

                for day_data in data[subject_code]:
                    for tick in day_data:
                        체결시간, 현재가, 영업일자 = parse_tick(tick)
                        kw.OnReceiveRealData(subject_code, 현재가, 체결시간)

                chart.clear_data(subject_code)

        running_time = running_time + (time.time() - s_time)
        log.info('테스트 종료.')
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def parse_tick(tick):
    return tick[0], tick[1], tick[2]

def get_simulate_count(subject_symbol):
    try:
        return 1
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))

def set_simulate_config(subject_code):
    try:
        pass
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))