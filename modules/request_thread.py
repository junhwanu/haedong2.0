# -*- coding: utf-8 -*-
import sys, os, threading, time
import log_manager as log
import kiwoom

rq_thread = None

def get_instance(ocx):
    global rq_thread

    try:
        if rq_thread is None or rq_thread.is_alive() is False:
            rq_thread = Request_thread(ocx)

        return rq_thread
    except Exception as err:
        log.error(err)

class Request_thread(threading.Thread):

    def __init__(self, ocx):
        self.ocx = ocx
        self.rq_list = []

    def push(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        try:
            self.rq_list.append({"sRQName":sRQName,
                                "sTrCode":sTrCode,
                                "nPrevNext":nPrevNext,
                                "sScreenNo":sScreenNo})
        except Exception as err:
            log.error(err)

    def run(self):
        try:
            while not len(self.rq_list):
                req = self.rq_list[0]

                rtn = self.ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", req['sRQName'], req['sTrCode'], req['nPrevNext'], req['sScreenNo'])

                if rtn == 0:
                    self.rq_list.pop(0);
                else:
                    log.error(kiwoom.Api().parse_error_code(rtn))

                time.sleep(0.3)
        except Exception as err:
            log.error(err)
