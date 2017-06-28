# -*- coding: utf-8 -*-
import datetime
import subject
import strategy_var as st
import log_manager
import constant as const

data = {}
log, res, err_log = log_manager.Log().get_logger()

def init_data(subject_code):
    data[subject_code] = {}

    data[subject_code]['상태'] = '대기'

    if subject.info[subject_code]['전략'] == '파라':
        for chart_config in st.info[subject_code]['파라']['차트']:
            chart_type = chart_config[0]
            time_unit = chart_config[1]

            if chart_type == const.틱차트:
                if const.틱차트 not in data[subject_code]:
                    data[subject_code][chart_type] = {}

                data[subject_code][chart_type][time_unit] = {}
                data[subject_code][chart_type][time_unit]['현재가'] = []
                data[subject_code][chart_type][time_unit]['시가'] = []
                data[subject_code][chart_type][time_unit]['고가'] = []
                data[subject_code][chart_type][time_unit]['저가'] = []
                data[subject_code][chart_type][time_unit]['체결시간'] = []
                data[subject_code][chart_type][time_unit]['영업일자'] = []
                data[subject_code][chart_type][time_unit]['거래량'] = []
                data[subject_code][chart_type][time_unit]['현재가변동횟수'] = 0
                data[subject_code][chart_type][time_unit]['현재캔들'] = {}
                data[subject_code][chart_type][time_unit]['임시캔들'] = []
                data[subject_code][chart_type][time_unit]['임시데이터'] = []
                data[subject_code][chart_type][time_unit]['임시틱'] = []
                data[subject_code][chart_type][time_unit]['차트타입'] = chart_type
                data[subject_code][chart_type][time_unit]['시간단위'] = time_unit

                data[subject_code][chart_type][time_unit]['인덱스'] = -1
                data[subject_code][chart_type][time_unit]['이동평균선'] = {}
                data[subject_code][chart_type][time_unit]['이동평균선']['일수'] = st.info[subject_code][subject.info[subject_code]['전략']]['차트변수'][chart_type][time_unit]['이동평균선']
                data[subject_code][chart_type][time_unit]['지수이동평균선'] = {}

                for days in data[subject_code][chart_type][time_unit]['이동평균선']['일수']:
                    data[subject_code][chart_type][time_unit]['이동평균선'][days] = []
                    data[subject_code][chart_type][time_unit]['지수이동평균선'][days] = []

                data[subject_code][chart_type][time_unit]['볼린저밴드'] = {}
                data[subject_code][chart_type][time_unit]['볼린저밴드']['중심선'] = []
                data[subject_code][chart_type][time_unit]['볼린저밴드']['상한선'] = []
                data[subject_code][chart_type][time_unit]['볼린저밴드']['하한선'] = []
                data[subject_code][chart_type][time_unit]['볼린저밴드']['캔들위치'] = []

                data[subject_code][chart_type][time_unit]['일목균형표'] = {}
                data[subject_code][chart_type][time_unit]['일목균형표']['전환선'] = []
                data[subject_code][chart_type][time_unit]['일목균형표']['기준선'] = []
                data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'] = []
                data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'] = []
                for index in range(0, 26):
                    data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)
                    data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)

                data[subject_code][chart_type][time_unit]['현재SAR'] = 0  # 현재 SAR
                data[subject_code][chart_type][time_unit]['SAR'] = []
                data[subject_code][chart_type][time_unit]['EP'] = 0
                data[subject_code][chart_type][time_unit]['AF'] = 0
                data[subject_code][chart_type][time_unit]['현재플로우'] = ''
                data[subject_code][chart_type][time_unit]['플로우'] = []
                data[subject_code][chart_type][time_unit]['지난플로우'] = []  # [ {'추세': '상향', '시작SAR': 1209.3 '마지막SAR': 1212.4 }, {'추세': '하향', '시작SAR': 1212.4 '마지막SAR': 1211.0 } ]
            elif chart_type is const.분차트:
                data[subject_code][chart_type][time_unit]['현재가변동시간'] = []
                pass

    else:
        '''
        data[subject_code][chart_type][time_unit]['일목균형표'] = {}
        data[subject_code][chart_type][time_unit]['일목균형표']['전환선'] = []
        data[subject_code][chart_type][time_unit]['일목균형표']['기준선'] = []
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'] = []
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'] = []
        for index in range(0, 26):
            data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)
            data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)
        '''

def clear_data(subject_code):
    del data[subject_code]

def init_current_candle(subject_code, chart_type, time_unit):
    data[subject_code][chart_type][time_unit]['현재캔들']['고가'] = 0
    data[subject_code][chart_type][time_unit]['현재캔들']['저가'] = const.INFINITY

    if chart_type is const.틱차트:
        data[subject_code][chart_type][time_unit]['현재가변동횟수'] = 0
    elif chart_type is const.분차트:
        data[subject_code][chart_type][time_unit]['현재가변동시간'] = '?????'


def push(subject_code, chart_type, time_unit, candle):
    data[subject_code][chart_type][time_unit]['현재가'].append(candle['현재가'])
    data[subject_code][chart_type][time_unit]['시가'].append(candle['시가'])
    data[subject_code][chart_type][time_unit]['고가'].append(candle['고가'])
    data[subject_code][chart_type][time_unit]['저가'].append(candle['저가'])
    data[subject_code][chart_type][time_unit]['체결시간'].append(candle['체결시간'])
    if '영업일자' in candle: data[subject_code][chart_type][time_unit]['영업일자'].append(candle['영업일자'])
    if '거래량' in candle: data[subject_code][chart_type][time_unit]['거래량'].append(candle['거래량'])
    data[subject_code][chart_type][time_unit]['인덱스'] += 1

    calc(subject_code, chart_type, time_unit)


def calc(subject_code, chart_type, time_unit):
    if subject.info[subject_code]['전략'] == '파라':
        calc_ma_line(subject_code, chart_type, time_unit)
        calc_ema_line(subject_code, chart_type, time_unit)
        #calc_ilmok_chart(subject_code, chart_type, time_unit)

        if data[subject_code][chart_type][time_unit]['인덱스'] < 5:
            data[subject_code][chart_type][time_unit]['플로우'].append('모름')
            data[subject_code][chart_type][time_unit]['SAR'].append(0)
        elif data[subject_code][chart_type][time_unit]['인덱스'] == 5:
            init_sar(subject_code, chart_type, time_unit)
        else:
            calc_sar(subject_code, chart_type, time_unit)


def calc_ma_line(subject_code, chart_type, time_unit):
    '''
    이동평균선 계산
    '''
    for days in data[subject_code][chart_type][time_unit]['이동평균선']['일수']:
        if data[subject_code][chart_type][time_unit]['인덱스'] >= days - 1:
            avg = sum(
                data[subject_code][chart_type][time_unit]['현재가'][
                data[subject_code][chart_type][time_unit]['인덱스'] - days + 1: data[subject_code][chart_type][time_unit][
                                                                                 '인덱스'] + 1]) / days
            data[subject_code][chart_type][time_unit]['이동평균선'][days].append(avg)
        else:
            data[subject_code][chart_type][time_unit]['이동평균선'][days].append(None)


def calc_ema_line(subject_code, chart_type, time_unit):
    '''
    지수이동평균선 계산
    '''
    for days in data[subject_code][chart_type][time_unit]['이동평균선']['일수']:
        if data[subject_code][chart_type][time_unit]['인덱스'] >= days - 1:
            if data[subject_code][chart_type][time_unit]['인덱스'] == days - 1:
                avg = sum(data[subject_code][chart_type][time_unit]['현재가'][
                          data[subject_code][chart_type][time_unit]['인덱스'] - days + 1:
                          data[subject_code][chart_type][time_unit]['인덱스'] + 1]) / days
                data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(avg)
            else:
                alpha = 2 / (days + 1)
                ema = alpha * data[subject_code][chart_type][time_unit]['현재가'][-1] + (1.0 - alpha) * \
                                                                                     data[subject_code][chart_type][
                                                                                         time_unit]['지수이동평균선'][days][-1]
                data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(ema)
        else:
            data[subject_code][chart_type][time_unit]['지수이동평균선'][days].append(None)


def calc_ilmok_chart(subject_code, chart_type, time_unit):
    '''
    일목균형표 계산
    '''
    if data[subject_code][chart_type][time_unit]['인덱스'] < 9:
        data[subject_code][chart_type][time_unit]['일목균형표']['전환선'].append(None)
    else:
        data[subject_code][chart_type][time_unit]['일목균형표']['전환선'].append((max(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 9: data[subject_code][chart_type][time_unit][
                '인덱스']]) + min(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 9: data[subject_code][chart_type][time_unit][
                '인덱스']])) / 2)

    if data[subject_code][chart_type][time_unit]['인덱스'] < 26:
        data[subject_code][chart_type][time_unit]['일목균형표']['기준선'].append(None)
    else:
        data[subject_code][chart_type][time_unit]['일목균형표']['기준선'].append((max(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 26: data[subject_code][chart_type][time_unit][
                '인덱스']]) + min(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 26: data[subject_code][chart_type][time_unit][
                '인덱스']])) / 2)

    if data[subject_code][chart_type][time_unit]['인덱스'] >= 26:
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append((data[subject_code][chart_type][time_unit][
                                                                                '일목균형표']['전환선'][
                                                                                data[subject_code][chart_type][
                                                                                    time_unit]['인덱스']] +
                                                                            data[subject_code][chart_type][time_unit][
                                                                                '일목균형표']['기준선'][
                                                                                data[subject_code][chart_type][
                                                                                    time_unit]['인덱스']]) / 2)
    else:
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬1'].append(None)

    if data[subject_code][chart_type][time_unit]['인덱스'] >= 52:
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append((max(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 52: data[subject_code][chart_type][time_unit][
                '인덱스']]) + min(
            data[subject_code][chart_type][time_unit]['현재가'][
            data[subject_code][chart_type][time_unit]['인덱스'] - 52: data[subject_code][chart_type][time_unit][
                '인덱스']])) / 2)
    else:
        data[subject_code][chart_type][time_unit]['일목균형표']['선행스팬2'].append(None)


def init_sar(subject_code, chart_type, time_unit):
    ep = data[subject_code][chart_type][time_unit]['EP']
    af = st.info[subject_code]['파라']['차트변수'][chart_type][time_unit]['INIT_AF']
    idx = data[subject_code][chart_type][time_unit]['인덱스']

    temp_high_price_list = []
    temp_low_price_list = []

    for i in range(idx):
        temp_high_price_list.append(data[subject_code][chart_type][time_unit]['고가'][i])
        temp_low_price_list.append(data[subject_code][chart_type][time_unit]['저가'][i])

    score = 0

    for i in range(len(temp_high_price_list) - 1):
        if temp_high_price_list[i] < temp_high_price_list[i + 1]:
            score = score + 1
        else:
            score = score - 1

    if score >= 1:
        init_sar = min(temp_low_price_list)
        temp_flow = "상향"
        ep = max(temp_high_price_list)
    if score < 1:
        init_sar = max(temp_high_price_list)
        ep = min(temp_low_price_list)
        temp_flow = "하향"

    sar = ((ep - init_sar) * af) + init_sar

    data[subject_code][chart_type][time_unit]['SAR'].append(sar)
    data[subject_code][chart_type][time_unit]['현재SAR'] = sar
    data[subject_code][chart_type][time_unit]['EP'] = ep
    data[subject_code][chart_type][time_unit]['AF'] = af
    data[subject_code][chart_type][time_unit]['현재플로우'] = temp_flow
    data[subject_code][chart_type][time_unit]['플로우'].append(temp_flow)

    calc_sar(subject_code, chart_type, time_unit)


def calc_sar(subject_code, chart_type, time_unit):
    sar = data[subject_code][chart_type][time_unit]['SAR'][-1]
    ep = data[subject_code][chart_type][time_unit]['EP']
    temp_flow = data[subject_code][chart_type][time_unit]['플로우'][-1]
    af = data[subject_code][chart_type][time_unit]['AF']
    init_af = st.info[subject_code]['파라']['차트변수'][chart_type][time_unit]['INIT_AF']
    max_af = st.info[subject_code]['파라']['차트변수'][chart_type][time_unit]['MAX_AF']
    index = data[subject_code][chart_type][time_unit]['인덱스']
    temp_sar = sar

    the_highest_price = 0
    the_lowest_price = 0

    if temp_flow == "상향":
        the_highest_price = ep
    if temp_flow == "하향":
        the_lowest_price = ep

    next_sar = temp_sar

    if temp_flow == "상향":
        if data[subject_code][chart_type][time_unit]['저가'][index] >= next_sar:  # 상승추세에서 저가가 내일의 SAR보다 높으면 하락이 유효
            today_sar = next_sar
            temp_flow = "상향"
            the_lowest_price = 0
            if data[subject_code][chart_type][time_unit]['고가'][index] > ep:  # 신고가 발생
                the_highest_price = data[subject_code][chart_type][time_unit]['고가'][index]
                ep = data[subject_code][chart_type][time_unit]['고가'][index]
                af = af + init_af
                if af > max_af:
                    af = max_af

        elif data[subject_code][chart_type][time_unit]['저가'][index] < next_sar:  # 상승추세에서 저가가 내일의 SAR보다 낮으면 하향 반전
            temp_flow = "하향"
            af = init_af
            today_sar = ep
            the_highest_price = 0
            the_lowest_price = data[subject_code][chart_type][time_unit]['저가'][index]

            ep = the_lowest_price
            log.info("%s, %s, %s : 하향 반전, 시간 : %s" % (
                subject_code, chart_type, time_unit, data[subject_code][chart_type][time_unit]['체결시간'][-1]))

            flow_result = {}
            flow_result['추세'] = const.상향
            flow_result['마지막SAR'] = next_sar
            if len(data[subject_code][chart_type][time_unit]['지난플로우']) == 0:
                flow_result['시작SAR'] = 0
            else:
                flow_result['시작SAR'] = data[subject_code][chart_type][time_unit]['지난플로우'][-1]['마지막SAR']

            data[subject_code][chart_type][time_unit]['지난플로우'].append(flow_result)

    elif temp_flow == "하향":
        if data[subject_code][chart_type][time_unit]['고가'][index] <= next_sar:  # 하락추세에서 고가가 내일의 SAR보다 낮으면 하락이 유효
            today_sar = next_sar
            temp_flow = "하향"
            the_highest_price = 0
            if data[subject_code][chart_type][time_unit]['저가'][index] < ep:  # 신저가 발생
                the_lowest_price = data[subject_code][chart_type][time_unit]['저가'][index]
                ep = data[subject_code][chart_type][time_unit]['저가'][index]
                af = af + init_af
                if af > max_af:
                    af = max_af

        elif data[subject_code][chart_type][time_unit]['고가'][index] > next_sar:  # 하락추세에서 고가가 내일의 SAR보다 높으면 상향 반전
            temp_flow = "상향"
            af = init_af
            today_sar = ep
            the_lowest_price = 0
            the_highest_price = data[subject_code][chart_type][time_unit]['고가'][index]

            ep = the_highest_price
            log.info("%s, %s, %s : 상향 반전, 시간 : %s" % (
                subject_code, chart_type, time_unit, data[subject_code][chart_type][time_unit]['체결시간'][-1]))

            flow_result = {}
            flow_result['추세'] = const.하향
            flow_result['마지막SAR'] = next_sar
            if len(data[subject_code][chart_type][time_unit]['지난플로우']) == 0:
                flow_result['시작SAR'] = 0
            else:
                flow_result['시작SAR'] = data[subject_code][chart_type][time_unit]['지난플로우'][-1]['마지막SAR']

            data[subject_code][chart_type][time_unit]['지난플로우'].append(flow_result)

    next_sar = today_sar + af * (max(the_highest_price, the_lowest_price) - today_sar)

    data[subject_code][chart_type][time_unit]['SAR'].append(next_sar)
    data[subject_code][chart_type][time_unit]['현재SAR'] = next_sar
    data[subject_code][chart_type][time_unit]['EP'] = ep
    data[subject_code][chart_type][time_unit]['AF'] = af
    data[subject_code][chart_type][time_unit]['현재플로우'] = temp_flow
    data[subject_code][chart_type][time_unit]['플로우'].append(temp_flow)
