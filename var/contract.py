# -*- coding: utf-8 -*-

class contract():
    종목코드 = ''
    매도수구분 = ''
    수량 = 0
    체결표시가격 = 0
    익절가 = [0]
    손절가 = [0]

    def __init__(self, params):
        if '종목코드' in params: self.종목코드 = params['종목코드']
        if '매도수구분' in params: self.매도수구분 = params['매도수구분']
        if '수량' in params: self.수량 = params['수량']
        if '체결표시가격' in params: self.체결표시가격 = params['체결표시가격']
        if '익절가' in params: self.익절가 = params['익절가']
        if '손절가' in params: self.손절가 = params['손절가']