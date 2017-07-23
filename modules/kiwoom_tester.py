# -*- coding: utf-8 -*-
import sys
import threading
import time

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *

import chart_manager as ctm
import constant as const
import contract_manager as cm
import log_manager
import screen
import strategy_manager as stm
import strategy_var as st
import subject
import telepot_manager as tm
import util
from log_manager import get_error_msg

log = None
res = None
err_log = None

class Api():
    chart = None
    stv = None
    누적수익 = 0

    def __init__(self, _stv = None):
        super(Api, self).__init__()
        global log, res, err_log
        log, res, err_log = log_manager.Log().get_logger()
        self.stv = _stv
        self.chart = ctm.Chart_Manger(self.stv)

    def send_order(self, contract_type, subject_code, contract_cnt):
        _contract_type = 0
        if contract_type == '신규매수':
            _contract_type = 2
        elif contract_type == '신규매도':
            _contract_type = 1
        else:
            return -300

        if const.MODE is const.REAL:
            return self.ocx.dynamicCall(
                "SendOrder(QString, QString, QString, int, QString, int, QString, QString, QString, QString)",
                [contract_type, '0101', self.account, _contract_type, subject_code, contract_cnt, '0', '0', '1', ''])
        elif const.MODE is const.TEST: # 테스트
            #tester.send_order(contract_type, subject_code, contract_cnt, '1')
            return 0

    ####################################################
    # Control Event Handlers
    ####################################################

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList, o_info=None):
        pass

    def OnReceiveRealData(self, subject_code, sRealType, sRealData):
        """
        실시간 시세 이벤트
        실시간데이터를 받은 시점을 알려준다.

        :param subject_code: 종목코드
        :param sRealType: 리얼타입
        :param sRealData: 실시간 데이터전문
        """
        print("test")
        try:
            if subject_code not in subject.info:
                #log.error("요청하지 않은 데이터 수신. (%s, %s, %s)" % (subject_code, sRealType, sRealData))
                return

            #res.info("RealData (%s, %s, %s)" % (subject_code, sRealType, sRealData))

            if const.MODE == const.REAL:
                current_price = self.ocx.dynamicCall("GetCommRealData(QString, int)", "현재가", 140)  # 140은 현재가의 코드
                current_time = self.ocx.dynamicCall("GetCommRealData(QString, int)", "체결시간", 20)  # 20은 체결시간의 코드
            elif const.MODE == const.TEST:
                current_price = sRealType
                current_time = sRealData

            current_price = round(float(current_price), subject.info[subject_code]['자릿수'])

            if const.MODE == const.REAL:
                ''' Send Request '''
                now = time.time()
                if now - self.last_req_time > 0.25:
                    self.send_request()
                    self.last_req_time = now

                ''' 계좌번호 비밀번호 입력했는지 체크 '''
                if now- self.last_pwd_check_time > 2 and self.account_pwd_input is False:
                    self.get_my_deposit_info()
                    self.get_contract_list()
                    self.last_pwd_check_time = now


            ''' 캔들 생성 '''
            for chart_config in st.info[subject_code][subject.info[subject_code]['전략']][const.차트]:
                chart_type = chart_config[0]
                time_unit = chart_config[1]

                chart_data = self.chart.data[subject_code][chart_type][time_unit]
                if chart_type == const.틱차트:
                    if len(chart_data['현재캔들'].keys()) is 0:
                        chart_data['임시틱'].append( [ current_price, current_time ])
                        return

                    if chart_data['현재가변동횟수'] == 0:
                        chart_data['현재캔들']['시가'] = current_price

                    chart_data['현재가변동횟수'] += 1
                    if current_price < chart_data['현재캔들']['저가'] : chart_data['현재캔들']['저가'] = current_price
                    if current_price > chart_data['현재캔들']['고가']: chart_data['현재캔들']['고가'] = current_price

                    if chart_data['현재가변동횟수'] == int(time_unit):
                        chart_data['현재캔들']['체결시간'] = current_time
                        chart_data['현재캔들']['현재가'] = current_price
                        chart_data['현재가변동횟수'] = 0
                        if chart_data['인덱스'] == -1 and const.MODE == const.REAL:
                            chart_data['임시캔들'].append(chart_data['현재캔들'])
                        else:
                            #log.info('%s, %s, %s, %s' % (subject_code, chart_type, time_unit, chart_data['현재캔들']))
                            self.chart.push(subject_code, chart_type, time_unit, chart_data['현재캔들'])

                        self.chart.init_current_candle(subject_code, chart_type, time_unit)

                elif chart_type == const.분차트:
                    pass

            ''' 계약 청산 '''
            if cm.get_contract_count(subject_code) > 0:
                sell_contents = stm.is_it_sell(subject_code, current_price)

                if sell_contents['신규주문']:
                    self.send_order(sell_contents['매도수구분'], subject_code, sell_contents['수량'])

            ''' 매매 진입 '''
            if cm.get_contract_count(subject_code) == 0:
                order_contents = stm.is_it_ok(subject_code, current_price)

                if order_contents['신규주문']:
                    res.info('신규주문 : %s' % order_contents)
                    res.info("체결시간:%s" % chart_data['체결시간'][-1])
                    self.send_order(order_contents['매도수구분'], subject_code, order_contents['수량'])

            ''' 전략 선택 '''
            stm.strategy_selector(subject_code, current_price)


        except Exception as err:
            log.error(get_error_msg(err))

    @staticmethod
    def parse_error_code(err_code):
        """
        Return the message of error codes

        :param err_code: Error Code
        :type err_code: str
        :return: Error Message
        """
        err_code = str(err_code)
        ht = {
            "0": "정상처리",
            "-100": "사용자정보교환에 실패하였습니다. 잠시후 다시 시작하여 주십시오.",
            "-101": "서버 접속 실패",
            "-102": "버전처리가 실패하였습니다.",
            "-200": "시세조회 과부하",
            "-201": "REQUEST_INPUT_st Failed",
            "-202": "요청 전문 작성 실패",
            "-300": "주문 입력값 오류",
            "-301": "계좌비밀번호를 입력하십시오.",
            "-302": "타인계좌는 사용할 수 없습니다.",
            "-303": "주문가격이 20억원을 초과합니다.",
            "-304": "주문가격은 50억원을 초과할 수 없습니다.",
            "-305": "주문수량이 총발행주수의 1%를 초과합니다.",
            "-306": "주문수량은 총발행주수의 3%를 초과할 수 없습니다."
        }
        return ht[err_code] + " (%s)" % err_code if err_code in ht else err_code



    ####################################################
    # Test Function
    ####################################################

    def receiveTestData(self, candle):

        # chart_manager 계산

        # 매매


        pass