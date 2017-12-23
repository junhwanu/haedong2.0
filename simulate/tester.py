# -*- coding: utf-8 -*-
import time
import configparser
import json
import subprocess
import var.subject as subject
import var.strategy_var as strategy_var
import manager.chart_manager as chart
import multiprocessing as mp
import os
from utils.util import *
from constant.constant import *
from modules.kiwoom_tester import *
from manager.db_manager import *
from manager.log_manager import LogManager


def simulate(stv, common_data):
    result = []
    try:
        print('%s simulate start.' % os.getpid())
        print('common_data keys() : %s' % common_data.keys())
        for key1 in common_data.keys():
            for key2 in common_data[key1].keys():
                for key3 in common_data[key1][key2].keys():
                    for key4 in common_data[key1][key2][key3].keys():
                        for data in common_data[key1][key2][key3][key4]:
                            print(data)

        record = {}
        profit = 0

        kiwoom_tester = KiwoomTester(stv)
        for subject_code in common_data.keys():
            log = kiwoom_tester.log
            kiwoom_tester.chart.init_data(subject_code, common_data)

            stv_info = kiwoom_tester.stv.info
            sbv_info = kiwoom_tester.subject_var.info
            chart_type = stv_info[subject_code][sbv_info[subject_code]][차트][0][0]
            time_unit = stv_info[subject_code][sbv_info[subject_code]][차트][0][1]
            for i in range(0, len(common_data[subject_code][chart_type][time_unit])):
                kiwoom_tester.chart.calc(subject_code, chart_type, 60)
                kiwoom_tester.chart.data[subject_code][chart_type][time_unit]['인덱스'] += 1
                print('process id : %s, candle index : %s' % (os.getpid(), i))
                order_info = kiwoom_tester.check_contract_in_candle(subject_code, chart_type, time_unit)

                if order_info[신규매매]:
                    kiwoom_tester.send_order(order_info[매도수구분], subject_code, order_info[수량])

            profit = profit + kiwoom_tester.누적수익

        record['전략변수'] = kiwoom_tester.stv
        record['누적수익'] = kiwoom_tester.누적수익

        result.append(record)
    except Exception as err:
        print(err)

class Tester:
    running_time = 0
    result = []

    log, res, err_log = None, None, None

    ctm = None

    def __init__(self):
        self.log, self.res, self.err_log = LogManager.__call__().get_logger()
        self.sbv = subject.Subject()

    def print(self):
        for i in range(0, 10):
            print(i)

    def proc(self):
        global running_time
        '''
        테스트 진입
        종목코드, 시작일, 종료일 받아옴
        '''
        dbm = DBManager()
        subject_symbol = ''
        start_date = ''
        end_date = ''
        self.log.info('종목코드를 입력하세요. [ ex) GC ]')
        subject_symbol = input()

        if subject_symbol not in self.sbv.info:
            self.log.info('잘못된 종목코드입니다.')
            self.proc()
            return

        self.log.info('시작일을 입력하세요.')
        start_date = input()
        if len(start_date) != 8:
            self.log.info('잘못된 시작일입니다.')
            self.proc()
            return

        self.log.info('종료일을 입력하세요.')
        end_date = input()
        if len(end_date) != 8:
            self.log.info('잘못된 종료일입니다.')
            self.proc()
            return

        '''
        입력 종료        '''

        try:
            ''' 해당 종목 테이블 가져옴 '''
            _tables = dbm.get_table_list(subject_symbol)
            tables = []
            for table_name in _tables:
                print(table_name[0], start_date, end_date)
                if dbm.is_matched_table(table_name[0], start_date, end_date):
                    tables.append(table_name[0])

            data = {}
            for table_name in tables:
                data[table_name] = []
                self.log.info('%s 월물 테이블 내용 수신 시작.' % table_name)
                data[table_name] = dbm.request_tick_candle(table_name, '60', start_date, end_date)
                print(data[table_name])
                '''
                TODO:
                현재 1가지 차트로만 고정 추후 여러 차트 가능하게 확장 예정
                '''

            self.start_date = start_date
            self.end_date = end_date
            self.subject_symbol = subject_symbol

            '''
            상단까지가 우리가 입력한 날짜에 맞는 테이블을 틱_60으로만 가져오는 코드
            '''

            with mp.Manager() as manager:
                result = manager.list()
                common_data = manager.dict()
                while True:
                    # self.log.info("DB 데이터를 설정된 차트에 맞는 캔들 데이터로 변환합니다.")
                    # data[subject_code] -> ctm.common_data에 setting
                    # tester_var.cfg에서 subject_symbol에 맞는 chart_type, time_unit을 가져와서 계산한다.

                    self.log.info("총 테스트 횟수를 계산합니다.")
                    total_count = 1
                    stv_table, cur_table = self.create_simulater_var_table()  # 총 테스트 횟수 계산
                    for cnt in stv_table:
                        total_count *= (cnt+1)

                    self.log.info("총 %s번의 테스트." % total_count)

                    label = subprocess.check_output(["git", "describe", "--always"]) # current git hash
                    procs = []

                    stv = self.calc_strategy_var(cur_table)

                    self.log.info("tables data : %s" % tables)
                    self.log.info("common data : %s" % common_data)
                    # 차트 수신
                    if len(common_data.keys()) == 0:
                        for subject_code in tables:
                            common_data[subject_code] = manager.dict()
                            for strategy in stv.info[subject_symbol]:
                                for chart_config in stv.info[subject_symbol][strategy][차트]:
                                    self.log.info('chart config : %s' % chart_config)
                                    self.log.info('subject_code : %s' % subject_code)
                                    if chart_config[0] not in common_data[subject_code].keys():
                                        common_data[subject_code][chart_config[0]] = manager.dict()
                                    if chart_config[1] not in common_data[subject_code][chart_config[0]].keys():
                                        common_data[subject_code][chart_config[0]][chart_config[1]] = manager.dict()
                                        common_data[subject_code][chart_config[0]][chart_config[1]][현재가] = manager.list()
                                        common_data[subject_code][chart_config[0]][chart_config[1]][고가] = manager.list()
                                        common_data[subject_code][chart_config[0]][chart_config[1]][저가] = manager.list()
                                        common_data[subject_code][chart_config[0]][chart_config[1]][시가] = manager.list()
                                        common_data[subject_code][chart_config[0]][chart_config[1]][체결시간] = manager.list()
                                        #data[subject_code] = dbm.request_tick_candle(subject_code, chart_config[1])
                                        for candle in data[subject_code][:100]:
                                            common_data[subject_code][chart_config[0]][chart_config[1]][
                                                현재가].append(candle[현재가])
                                            common_data[subject_code][chart_config[0]][chart_config[1]][
                                                고가].append(candle[고가])
                                            common_data[subject_code][chart_config[0]][chart_config[1]][
                                                저가].append(candle[저가])
                                            common_data[subject_code][chart_config[0]][chart_config[1]][
                                                시가].append(candle[시가])
                                            common_data[subject_code][chart_config[0]][chart_config[1]][
                                                체결시간].append(candle[체결시간])
                                            #self.log.info("candle append.")

                    self.log.info("common data : %s" % common_data)
                    while True:
                        stv = self.calc_strategy_var(cur_table)

                        ''' 해당 부분에서 Multiprocessing으로 테스트 시작 '''
                        process = mp.Process(target=simulate, args=(stv, common_data, ))
                        procs.append(process)
                        process.start()

                        break
                        if self.increase_the_number_of_digits(stv_table, cur_table) == False: break

                    for process in procs:
                        process.join()

                    self.log.info("[테스트 결과]")

                    ''' 이 부분에 result를 수익별로 sorting '''

                    ''' 상위 N개의 결과 보여 줌 '''
                    print(len(result))
                    for i in range(0, min(len(result), 10)):
                        self.log.info(result[i]) # 더 디테일하게 변경

                    self.log.info("해당 코드의 Git Hash : %s" % label)
                    while True:
                        self.log.info("Database에 넣을 결과 Index를 입력해주세요.(종료 : -1)")
                        idx = input()
                        if idx == '-1': break
                        self.log.info("저장하신 결과에 대한 코드를 나중에 확인하시기 위해선, 코드를 변경하시기 전에 Commit을 해야 합니다.")

                        ''' 해당 index의 결과를 stv를 정렬해서, 결과 DB에 저장. '''

                    self.log.info("Config를 변경하여 계속 테스트 하시려면 아무키나 눌러주세요.(종료 : exit)")
                    cmd = input()
                    if cmd == 'exit': break

            self.log.info('테스트 종료.')

        except Exception as err:
            self.err_log.error(get_error_msg(err))


    def parse_tick(tick):
        return tick[0], tick[1], tick[2]

    def increase_the_number_of_digits(self, max_array, cur_array):
        cur_array[-1] += 1
        for i in range(len(cur_array)-1 , -1, -1):
            if cur_array[i] > max_array[i]:
                if i == 0:
                    return False
                cur_array[i] = 0
                cur_array[i-1] += 1
            else: break
        return True

    def calc_divide_count(self, start, end, interval):
        ''' [10, 40, 5] 일 경우 6을 return 해주는 코드, [0, 0, 0]이면 1이아니라 0을 리턴한다.
            테스트 stv의 max_array를 만들기 위해 사용 됨 '''
        if start == end: return 0
        if interval == 0: return 0
        return int((end - start) / interval)

    def get_divide_value(self, sei_list, index):
        ''' start, end, interval list = sei_list '''
        return sei_list[0] + (sei_list[2] * index)

    def calc_strategy_var(self, _cur_array):

        try:
            cur_array = _cur_array[:]
            # 전략 변수 Config 불러오기
            config = configparser.RawConfigParser()
            config.read(CONFIG_PATH + '/tester_var.cfg')
            stv = strategy_var.Strategy_Var()

            for subject_code in self.sbv.info.keys():
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
                    stv.info[subject_symbol][strategy][차트변수][매매불가수익량] = self.get_divide_value(json.loads(config.get(subject_symbol, 매매불가수익량)), cur_array.pop(0))
                    tmp_list = json.loads(config.get(subject_symbol, 청산단계별드리블틱))
                    stv.info[subject_symbol][strategy][차트변수][청산단계별드리블틱] = []
                    for list in tmp_list:
                        stv.info[subject_symbol][strategy][차트변수][청산단계별드리블틱].append(self.get_divide_value(list, cur_array.pop(0)))

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
                            stv.info[subject_symbol][strategy][차트변수][type][time_unit][이동평균선].append(self.get_divide_value(list, cur_array.pop(0)))

                        stv.info[subject_symbol][strategy][차트변수][type][time_unit][INIT_AF] = self.get_divide_value(
                            json.loads(config.get(section_str, INIT_AF)), cur_array.pop(0))

                        stv.info[subject_symbol][strategy][차트변수][type][time_unit][MAX_AF] = self.get_divide_value(
                            json.loads(config.get(section_str, MAX_AF)), cur_array.pop(0))

                        stv.info[subject_symbol][strategy][차트변수][type][time_unit][초기캔들수] = self.get_divide_value(
                            json.loads(config.get(section_str, 초기캔들수)), cur_array.pop(0))

            return stv
        except Exception as err:
            self.err_log.error(get_error_msg(err))


    def create_simulater_var_table(self):
        try:
            max_array = []
            cur_array = []
            # 전략 변수 Config 불러오기
            config = configparser.RawConfigParser()
            config.read(CONFIG_PATH + '/tester_var.cfg')

            for subject_code in self.sbv.info.keys():
                subject_symbol = subject_code[:2]

                strategy = config.get(ST_CONFIG, subject_symbol)

            if strategy == 파라:
                tmp_list = json.loads(config.get(subject_symbol, 매매불가수익량))
                max_array.append(self.calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                cur_array.append(0)

                tmp_list = json.loads(config.get(subject_symbol, 청산단계별드리블틱))
                for list in tmp_list:
                    max_array.append(self.calc_divide_count(list[0], list[1], list[2]))
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
                            max_array.append(self.calc_divide_count(list[0], list[1], list[2]))
                            cur_array.append(0)
                        tmp_list = json.loads(config.get(section_str, INIT_AF))
                        max_array.append(self.calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                        cur_array.append(0)
                        tmp_list = json.loads(config.get(section_str, MAX_AF))
                        max_array.append(self.calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                        cur_array.append(0)
                        tmp_list = json.loads(config.get(section_str, 초기캔들수))
                        max_array.append(self.calc_divide_count(tmp_list[0], tmp_list[1], tmp_list[2]))
                        cur_array.append(0)

            return max_array, cur_array
        except Exception as err:
            self.err_log.error(get_error_msg(err))
            return None, None

    def set_simulate_config(self, subject_code):

        try:
            # 전략 변수 Config 불러오기
            config = configparser.RawConfigParser()
            config.read(CONFIG_PATH + '/tester_var.cfg')

            stv = strategy_var()
            for subject_code in self.sbv.info.keys():
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
            self.err_log.error(get_error_msg(err))