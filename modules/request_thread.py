# -*- coding: utf-8 -*-
import threading, time
import log_manager
from PyQt5 import QtGui, QtCore

input_value = []
rq_list = []
ocx = None
log, res = log_manager.Log().get_logger()
rq_thread = None

def init(_ocx):
    global ocx, log, res, rq_thread

    try:
        ocx = _ocx
        #request_func()
        rq_thread = Request_thread()

    except Exception as err:
        log.error(err)

def set_input_value(sID, sValue):
    global rq_list, input_value
    log.debug("set input value, id : %s, value : %s" % (sID, sValue))
    input_value.append([sID, sValue])
    log.debug("input value : %s" % input_value)

def push(sRQName, sTrCode, nPrevNext, sScreenNo):
    global rq_list, input_value, log, res
    global rq_thread
    try:
        log.debug("push, input value : %s" % input_value)
        rq_list.append({
                        "inputValue":input_value,
                        "sRQName":sRQName,
                        "sTrCode":sTrCode,
                        "nPrevNext":nPrevNext,
                        "sScreenNo":sScreenNo})

        input_value = []
        #request_func()
        if not rq_thread.isRunning():
            rq_thread.start()
    except Exception as err:
        log.error(err)

def request_func(interval = 0.3):
    global log

    #log.debug("start request function().")
    if len(rq_list) > 0:
        req = rq_list[0]

        for input_value in req["inputValue"]:
            log.debug("set input value, id : %s, value : %s" % (input_value[0], input_value[1]))
            ocx.dynamicCall("SetInputValue(QString, QString)", input_value[0], input_value[1])

        log.debug("current thread : %s" % threading.current_thread().__class__.__name__)
        log.debug("req : %s" % req)
        rtn = ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", req['sRQName'], req['sTrCode'],
                                   req['nPrevNext'], req['sScreenNo'])

        log.debug("ocx.dynamicCall return value : %s" % rtn)
        if rtn == 0:
            rq_list.pop(0);
        else:
            # self.rq_list.pop(0);
            log.error(parse_error_code(rtn))

            if rtn == -200:
                # 시세조회 과부하
                pass
            elif rtn == -301:
                # 계좌비밀번호 입력
                pass

    time.sleep(0.3)

    #threading.Timer(interval, request_func, [interval]).start()

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

class Request_thread(QtCore.QThread):
    global rq_list, input_value, log, res, ocx

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        log.debug("init Request_thread")

    def run(self):
        while len(rq_list) > 0:
            req = rq_list[0]

            for input_value in req["inputValue"]:
                log.debug("set input value, id : %s, value : %s" % (input_value[0], input_value[1]))
                ocx.dynamicCall("SetInputValue(QString, QString)", input_value[0], input_value[1])

            log.debug("current thread : %s" % threading.current_thread().__class__.__name__)
            log.debug("req : %s" % req)
            rtn = ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", req['sRQName'], req['sTrCode'],
                                  req['nPrevNext'], req['sScreenNo'])

            log.debug("ocx.dynamicCall return value : %s" % rtn)
            if rtn == 0:
                rq_list.pop(0);
            else:
                # self.rq_list.pop(0);
                log.error(parse_error_code(rtn))

                if rtn == -200:
                    # 시세조회 과부하
                    pass
                elif rtn == -301:
                    # 계좌비밀번호 입력
                    pass

            time.sleep(3)


