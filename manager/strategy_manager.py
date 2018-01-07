# -*- coding: utf-8 -*-
import configparser
import json
import os

from constant import constant as const
from strategy import para
from utils import util
from var import strategy_var as stv

from manager.__manager import ManagerClass


class StrategyManager(ManagerClass):

    stv = stv.Strategy_Var()
    strategys = {}
    def __init__(self, stv, sbv, chart):
        super(StrategyManager, self).__init__()
        self.sbv = sbv
        self.chart = chart

    def get_strategy_var_from_config(self):
        stv = self.stv
        MODULE_PATH = os.path.dirname(os.path.abspath(__file__).replace('\\', '/'))

        try:
            # 전략 변수 Config 불러오기
            config = configparser.RawConfigParser()
            config.read(MODULE_PATH + '/strategy_var.cfg')

            for subject_code in self.sbv.info.keys():
                subject_symbol = subject_code[:2]

                if subject_symbol not in stv.info:
                    stv.info[subject_symbol] = {}

                strategy = config.get(const.ST_CONFIG, subject_symbol)
                stv.info[subject_symbol][strategy] = {}

                stv.info[subject_symbol][strategy][const.차트] = []
                stv.info[subject_symbol][strategy][const.차트변수] = {}
                stv.info[subject_symbol][strategy][const.차트변수][const.틱차트] = {}
                stv.info[subject_symbol][strategy][const.차트변수][const.분차트] = {}

                if strategy == const.파라:
                    stv.info[subject_symbol][strategy][const.차트변수][const.매매불가수익량] = config.get(subject_symbol, const.매매불가수익량)
                    stv.info[subject_symbol][strategy][const.차트변수][const.청산단계별드리블틱] \
                        = json.loads(config.get(subject_symbol, const.청산단계별드리블틱))

                # subject_symbol의 config 불러옴
                chart_types = json.loads(config.get(subject_symbol, const.CHART_TYPE))

                for chart_type in chart_types:
                    type_ = chart_type.split('_')[0]
                    time_unit = chart_type.split('_')[1]

                    section_str = subject_symbol + '_' + chart_type
                    stv.info[subject_symbol][strategy][const.차트변수][type_][time_unit] = {}
                    stv.info[subject_symbol][strategy][const.차트].append([str(type_), str(time_unit)])

                    if strategy == const.파라:
                        stv.info[subject_symbol][strategy][const.차트변수][type_][time_unit][const.이동평균선]\
                            = json.loads(config.get(section_str, const.이동평균선))
                        stv.info[subject_symbol][strategy][const.차트변수][type_][time_unit][const.INIT_AF]\
                            = config.getfloat(section_str, const.INIT_AF)
                        stv.info[subject_symbol][strategy][const.차트변수][type_][time_unit][const.MAX_AF]\
                            = config.getfloat(section_str, const.MAX_AF)
                        stv.info[subject_symbol][strategy][const.차트변수][type_][time_unit][const.초기캔들수]\
                            = config.getint(section_str, const.초기캔들수)

        except Exception as err:
            self.err_log.error(util.get_error_msg(err))

        return stv

    def get_strategy(self, subject_code):
        strategy = None
        stv = self.stv
        sbv = self.sbv
        chart = self.chart

        if self.sbv.info[subject_code][const.전략] == const.파라:
            if const.파라 not in self.strategys.keys():
                self.strategys[const.파라] = para.Para(stv, sbv, chart)
                return self.strategys[const.파라]
            else: return self.strategys[const.파라]
        else:
            self.err_log.error("전략 설정 에러.")
        return strategy

    def strategy_selector(self, subject_code, current_price):
        pass

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
