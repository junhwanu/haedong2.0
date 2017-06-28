# -*- coding: utf-8 -*-
import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))[:-9]

DB_SERVER_ADDR = "211.253.28.132"
DB_USER_ID = "root"
DB_USER_PWD = "goehddl"
DB_NAME = "haedong"
DB_CHARSET = "utf8"

MODE = None
REAL = 1
TEST = 2

FETCH_ONE = 0
FETCH_ALL = 1
FETCH_MANY = 2

CURSOR_TUPLE = 0
CURSOR_DICT = 1

틱차트 = "틱차트"
분차트 = "분차트"
일차트 = "일차트"

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
매매불가수익량 = "매매불가수익량"
맞 = "맞"
틀 = "틀"
청산단계별드리블틱 = "청산단계별드리블틱"

파라 = "파라"
현재SAR = "현재SAR"

분할 = 0
증가 = 1

INFINITY = 99999999
ZERO = 0