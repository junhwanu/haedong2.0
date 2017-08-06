# -*- coding: utf-8 -*-
import datetime, time
import constant as const
import chart_manager as chart
import strategy_var as st
import subject
import sys
import os

def get_today_date():
    today = datetime.date.today()
    year = str(today.year)
    month = str(today.month)
    if len(month) == 1: month = '0' + month

    day = str(today.day)
    if len(day) == 1: day = '0' + day

    return year + month + day


def get_time(add_min, subject_code):
    # 현재 시간 정수형으로 return
    if const.MODE== const.REAL:  # 실제투자
        current_hour = time.localtime().tm_hour
        current_min = time.localtime().tm_min + add_min

        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour * 100 + current_min

    elif const.MODE == const.TEST:  # 테스트
        sbv = subject.Subject()
        chart_type = st.info[subject_code][ sbv.info[subject_code]['전략'] ][const.차트][0][0]
        time_unit = st.info[subject_code][ sbv.info[subject_code]['전략'] ][const.차트][0][1]
        chart_data = chart.data[subject_code][chart_type][time_unit]

        current_hour = int(str(chart_data['체결시간'][-1])[8:10])
        current_min = int(str(chart_data['체결시간'][-1])[10:12]) + add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour * 100 + current_min

    return int(current_time)

def is_sorted(subject_code, chart_type, time_unit):
    lst = st.info[subject_code][const.파라]['차트변수'][chart_type][time_unit]['이동평균선']
    차트 = chart.data[subject_code][chart_type][time_unit]

    if max(lst) - 1 > 차트['인덱스']:
        return '모름'

    lst_real = []
    lst_tmp = []
    for days in lst:
        lst_real.append(차트['이동평균선'][days][차트['인덱스']])

    lst_tmp = lst_real[:]
    lst_tmp.sort()
    if lst_real == lst_tmp:
        return '하락세'

    lst_tmp.reverse()
    if lst_real == lst_tmp:
        return '상승세'

    return '모름'

def get_error_msg(err):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return "%s %s %s %s" % (err, exc_type, fname, exc_tb.tb_lineno)

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