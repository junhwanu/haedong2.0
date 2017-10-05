# -*- coding: utf-8 -*-
import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))[:-9]
CONFIG_PATH = MAIN_DIR + '/config'

## config
ST_CONFIG = 'STRATEGY_CONFIG'
CHART_TYPE = 'CHART_TYPE'

DB_SERVER_ADDR = "211.253.10.91"
DB_USER_ID = "root"
DB_USER_PWD = "goehddl"
DB_NAME = "haedong4"
DB_CHARSET = "utf8"

MODE = None
REAL = 1
TEST = 2

FETCH_ONE = 0
FETCH_ALL = 1
FETCH_MANY = 2

CURSOR_TUPLE = 0
CURSOR_DICT = 1

틱차트 = "TICK"
분차트 = "MIN"
일차트 = "DAY"

매도 = "신규매도"
매수 = "신규매수"

하락세 = "하락세"
상승세 = "상승세"

상향 = "상향"
하향 = "하향"
매매없음 = "매매없음"
추세 = "추세"
시작SAR = "시작SAR"
마지막SAR = "마지막SAR"
매매불가수익량 = "NOT_TRADE_PROFIT"
맞 = "맞"
틀 = "틀"
청산단계별드리블틱 = "DRIBLE_TICK"
차트 = "CHART"
차트변수 = "CHART_VAR"
파라 = "PARA"
현재SAR = "현재SAR"

이동평균선 = "MA"
INIT_AF = 'INIT_AF'
MAX_AF = 'MAX_AF'
초기캔들수 = 'INIT_CANDLE_COUNT'

분할 = 0
증가 = 1

시가 = "open"
저가 = "low"
고가 = "high"
현재가 = "close"
체결시간 = "date"
매도수구분 = "매도수구분"
신규주문 = "신규주문"
단위 = "단위"
현재플로우 = "현재플로우"
전략 = "전략"
신규매매 = "신규매매"
수량 = "수량"
false = {신규주문: False}

INFINITY = 99999999
ZERO = 0
