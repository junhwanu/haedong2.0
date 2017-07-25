# -*- coding: utf-8 -*-
import subject
import time
import strategy_var as st
import kiwoom
import constant as const
from db_manager import *
import log_manager
import chart_manager as chart
import configparser
import json
from strategy_var import Strategy_Var
from multiprocessing import Process, Queue
from kiwoom_tester import *
import subprocess

log, res, err_log = log_manager.Log().get_logger()
running_time = 0
result = []


def simulate(kw, result):
    record = {}
    chart_data = kw.chart.data
    stv_info = kw.stv.info
    subject_list = stv_info.keys()
    chart_type = {}
    time_unit = {}
    for subject_code in subject_list:
        chart_type[subject_code] = stv_info[subject_code]['전략찾아서넣고'][차트][0][0]
        time_unit[subject_code] = stv_info[subject_code]['전략찾아서넣고'][차트][0][1]

    for idx in range(0, chart_data):
        '''
        
        '''
        pass


def proc():
    global running_time
    dbm = DBManager()
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
        tables = dbm.get_table_list(subject_symbol, start_date, end_date)
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
                data[subject_code].append(dbm.get_table(table_name))

        while True:
            log.info("DB 데이터를 설정된 차트에 맞는 캔들 데이터로 변환합니다.")
            # data[subject_code] -> ctm.common_data에 setting
            # tester_var.cfg에서 subject_symbol에 맞는 chart_type, time_unit을 가져와서 계산한다.

            result['시작일'] = start_date
            result['종료일'] = end_date
            result['종목코드'] = subject_symbol

            log.info("총 테스트 횟수를 계산합니다.")
            total_count = 1
            stv_table, cur_table = create_simulater_var_table()  # 총 테스트 횟수 계산
            for cnt in stv_table:
                total_count * (cnt+1)

            log.info("총 %s번의 테스트." % total_count)

            label = subprocess.check_output(["git", "describe", "--always"]) # current git hash
            procs = []
            while True:
                stv = calc_strategy_var(cur_table)
                print(stv.info)
                kw_tester = KiwoomTester(stv)

                ''' 해당 부분에서 Multiprocessing으로 테스트 시작 '''
                '''
                process = Process(target=simulate(), args=(kw,))
                procs.append(process)
                process.start()
                '''
                if increase_the_number_of_digits(stv_table, cur_table) == False: break

            # for process in procs:
            #    process.join()

            log.info("[테스트 결과]")

            ''' 이 부분에 result를 수익별로 sorting '''

            ''' 상위 N개의 결과 보여 줌 '''
            for i in range(0, 10):
                log.info(result[i]) # 더 디테일하게 변경

            log.info("해당 코드의 Git Hash : %s" % label)
            while True:
                log.info("Database에 넣을 결과 Index를 입력해주세요.(종료 : -1)")
                idx = input()
                if idx == -1: break
                log.info("저장하신 결과에 대한 코드를 나중에 확인하시기 위해선, 코드를 변경하시기 전에 Commit을 해야 합니다.")

                ''' 해당 index의 결과를 stv를 정렬해서, 결과 DB에 저장. '''

            log.info("Config를 변경하여 계속 테스트 하시려면 아무키나 눌러주세요.(종료 : exit)")
            cmd = input()
            if cmd == 'exit': break

        log.info('테스트 종료.')
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))


def parse_tick(tick):
    return tick[0], tick[1], tick[2]

def increase_the_number_of_digits(max_array, cur_array):
    cur_array[-1] += 1
    for i in range(len(cur_array)-1 , -1, -1):
        if cur_array[i] > max_array[i]:
            if i == 0:
                return False
            cur_array[i] = 0
            cur_array[i-1] += 1
        else: break
    return True

def calc_divide_count(start, end, interval):
    ''' [10, 40, 5] 일 경우 6을 return 해주는 코드, [0, 0, 0]이면 1이아니라 0을 리턴한다.
        테스트 stv의 max_array를 만들기 위해 사용 됨 '''
    if start == end: return 0
    if interval == 0: return 0
    return int((end - start) / interval)

def get_divide_value(sei_list, index):
    ''' start, end, interval list = sei_list '''
    return sei_list[0] + (sei_list[2] * index)

def calc_strategy_var(_cur_array):

    try:
        cur_array = _cur_array[:]
        # 전략 변수 Config 불러오기
        config = configparser.RawConfigParser()
        config.read(CONFIG_PATH + '/tester_var.cfg')
        stv = Strategy_Var()

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
                stv.info[subject_symbol][strategy][차트변수][매매불가수익량] = get_divide_value(json.loads(config.get(subject_symbol, 매매불가수익량)), cur_array.pop(0))
                tmp_list = json.loads(config.get(subject_symbol, 청산단계별드리블틱))
                stv.info[subject_symbol][strategy][차트변수][청산단계별드리블틱] = []
                for list in tmp_list:
                    stv.info[subject_symbol][strategy][차트변수][청산단계별드리블틱].append(get_divide_value(list, cur_array.pop(0)))

            ## subject_symbol의 config 불러옴
            chart_types = json.loads(config.get(subject_symbol, CHART_TYPE))

            for chart_type in chart_types:
                type = chart_type.split('_')[0]
                time_unit = chart_type.split('_')[1]

                section_str = subject_symbol + '_' + chart_type
                stv.info[subject_symbol][strategy][차트변수][type][time_unit] = {}
                stv.info[subject_symbol][strategy][차트].append( [ str(type), str(time_unit) ] )
                if strategy == 파라:
                    tmp_list = json.loads(config.get(section_str, 이동평균선))
                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][이동평균선] = []
                    for list in tmp_list:
                        stv.info[subject_symbol][strategy][차트변수][type][time_unit][이동평균선].append(get_divide_value(list, cur_array.pop(0)))

                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][INIT_AF] = get_divide_value(
                        json.loads(config.get(section_str, INIT_AF)), cur_array.pop(0))

                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][MAX_AF] = get_divide_value(
                        json.loads(config.get(section_str, MAX_AF)), cur_array.pop(0))

                    stv.info[subject_symbol][strategy][차트변수][type][time_unit][초기캔들수] = get_divide_value(
                        json.loads(config.get(section_str, 초기캔들수)), cur_array.pop(0))

        return stv
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))


def create_simulater_var_table():
    try:
        max_array = []
        cur_array = []
        # 전략 변수 Config 불러오기
        config = configparser.RawConfigParser()
        config.read(CONFIG_PATH + '/tester_var.cfg')

        for subject_code in subject.info.keys():
            subject_symbol = subject_code[:2]

            strategy = config.get(ST_CONFIG, subject_symbol)

            if strategy == 파라:
                tmp_list = json.loads(config.get(subject_symbol, 매매불가수익량))
                max_array.append(calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                cur_array.append(0)

                tmp_list = json.loads(config.get(subject_symbol, 청산단계별드리블틱))
                for list in tmp_list:
                    max_array.append(calc_divide_count(list[0], list[1], list[2]))
                    cur_array.append(0)

            ## subject_symbol의 config 불러옴
            chart_types = json.loads(config.get(subject_symbol, CHART_TYPE))

            for chart_type in chart_types:
                type = chart_type.split('_')[0]
                time_unit = chart_type.split('_')[1]

                section_str = subject_symbol + '_' + chart_type
                if strategy == 파라:
                    tmp_list = json.loads(config.get(section_str, 이동평균선))
                    for list in tmp_list:
                        max_array.append(calc_divide_count(list[0], list[1], list[2]))
                        cur_array.append(0)
                    tmp_list = json.loads(config.get(section_str, INIT_AF))
                    max_array.append(calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                    cur_array.append(0)
                    tmp_list = json.loads(config.get(section_str, MAX_AF))
                    max_array.append(calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                    cur_array.append(0)
                    tmp_list = json.loads(config.get(section_str, 초기캔들수))
                    max_array.append(calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                    cur_array.append(0)

        return max_array, cur_array
    except Exception as err:
        err_log.error(log_manager.get_error_msg(err))
        return None, None

def set_simulate_config(subject_code):

    try:
        # 전략 변수 Config 불러오기
        config = configparser.RawConfigParser()
        config.read(CONFIG_PATH + '/tester_var.cfg')

        stv = Strategy_Var()
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