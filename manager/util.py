# -*- coding: utf-8 -*-
import datetime, time
import constant as const
import chart_manager as chart
import strategy_var as st
import subject

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
        chart_type = st.info[subject_code][ subject.info[subject_code]['전략'] ]['차트'][0][0]
        time_unit = st.info[subject_code][ subject.info[subject_code]['전략'] ]['차트'][0][1]
        chart_data = chart.data[subject_code][chart_type][time_unit]

        current_hour = int(str(chart_data['체결시간'][-1])[8:10])
        current_min = int(str(chart_data['체결시간'][-1])[10:12]) + add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour * 100 + current_min

    return int(current_time)

def get_previous_para_result(subject_code, chart_type, time_unit, length = 1):
    result = []

    return result

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