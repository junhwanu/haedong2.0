# -*- coding: utf-8 -*-
import sys, time, os

import constant as const
import screen
import util
import subject
import request_thread as rq_thread
import log_manager
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication

log = None
res = None

class Api():

    app = None
    account = ""

    def __init__(self):

        super(Api, self).__init__()
        global log, res
        log, res = log_manager.Log().get_logger()

        if const.MODE is const.REAL:
            log.info("해동이2.0 실제투자 시작 합니다.")
            self.app = QApplication(sys.argv)
            self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
            self.ocx.OnEventConnect[int].connect(self.OnEventConnect)
            self.ocx.OnReceiveTrData[str, str, str, str, str].connect(self.OnReceiveTrData)
            self.ocx.OnReceiveChejanData[str, int, str].connect(self.OnReceiveChejanData)
            self.ocx.OnReceiveRealData[str, str, str].connect(self.OnReceiveRealData)

            rq_thread.init(self.ocx)
            if self.connect() == 0:
                self.app.exec_()


        elif const.MODE is const.TEST:
            pass

        else:
            log.info("MODE:"+str(const.MODE))


    ####################################################
    # Interface Methods
    ####################################################

    def connect(self):
        """
        로그인 윈도우를 실행한다.
        로그인이 성공하거나 실패하는 경우 OnEventConnect 이벤트가 발생하고 이벤트의 인자 값으로 로그인 성공 여부를 알 수 있다.

        :return: 0 - 성공, 음수값은 실패
        """

        if self.ocx.dynamicCall("GetConnectState()") == 0:
            rtn = self.ocx.dynamicCall("CommConnect(1)")
            if rtn == 0:
                log.info("연결 성공")
            else:
                log.info("연결 실패")

            return rtn

    def get_login_info(self, sTag):
        """
        로그인한 사용자 정보를 반환한다.

        :param sTag: 사용자 정보 구분 TAG값
            “ACCOUNT_CNT” ? 전체 계좌 개수를 반환한다.
            "ACCNO" ? 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
            “USER_ID” - 사용자 ID를 반환한다.
            “USER_NAME” ? 사용자명을 반환한다.
            “KEY_BSECGB” ? 키보드보안 해지여부. 0:정상, 1:해지
            “FIREW_SECGB” ? 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
            Ex) openApi.GetLoginInfo(“ACCOUNT_CNT”);
        :return: TAG값에 따른 데이터 반환
        """
        return self.ocx.dynamicCall("GetLoginInfo(QString)", [sTag]).rstrip(';')

    def get_dynamic_subject_code(self):
        lists = ['MTL', 'ENG', 'CUR', 'IDX', 'CMD']
        for list in lists:
            self.set_input_value("상품코드", list)
            self.comm_rq_data("상품별현재가조회", "opt10006", "", screen.S0010)

    def get_dynamic_subject_market_time(self):
        lists = ['MTL', 'ENG', 'CUR', 'IDX', 'CMD']
        for list in lists:
            self.set_input_value("품목구분", list)
            self.comm_rq_data("장운영정보조회", "opw50001", "", screen.S0011)

    def get_contract_list(self):
        self.set_input_value("계좌번호", self.account)
        self.set_input_value("비밀번호", "")
        self.set_input_value("비밀번호입력매체", "00")
        self.set_input_value("통화코드", "")
        self.comm_rq_data("미결제잔고내역조회", "opw30003", "", screen.S0012)

    def get_my_deposit_info(self):
        self.set_input_value("계좌번호", self.account)
        self.set_input_value("비밀번호", "")
        self.set_input_value("비밀번호입력매체", "00")
        self.comm_rq_data("예수금및증거금현황조회", "opw30009", "", screen.S0011)

    def get_futures_deposit(self):
        lists = ['MTL', 'ENG', 'CUR', 'IDX', 'CMD']
        today = util.get_today_date()
        for list in lists:
            self.set_input_value("품목구분", list)
            self.set_input_value("적용일자", today)
            self.comm_rq_data("상품별증거금조회", "opw20004", "", screen.S0011)

    def send_order(self, contract_type, subject_code, contract_cnt):

        """
        주식 주문을 서버로 전송한다.
        신규매수:self.send_order("신규매수","0101",my_account_number,1,subject_code,1,now_current_price,"","2","")


        신규매도:
        매수청산:
       매도청산:self.send_order("신규매수","0101",my_account_number,2,subject_code,subject_info[subject_code]['보유수량'],now_current_price,"2","")


        :param sRQName: 사용자 구분 요청 명
        :param sScreenNo: 화면번호[ㄱ4]
        :param sAccNo: 계좌번호[10]
        :param nOrderType: 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매 도정정)
        :param sCode: 주식종목코드
        :param nQty: 주문수량
        :param sPrice: 주문단가
        :param sStop: 스탑단가
        :param sHogaGb: 거래구분 1:시장가, 2:지정가, 3:STOP, 4:STOP LIMIT

            ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
            ex)
            지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 48500, “00”, “”);
            시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0, “03”, “”);
            매수 정정 - openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 5, “000660”, 10, 49500, “00”, “1”);
            매수 취소 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 3, “000660”, 10, 0, “00”, “2”);
        :param sOrgOrderNo: 원주문번호
        :return: 에러코드 - parse_error_code
            -201     : 주문과부하
            -300     : 주문입력값 오류
            -301     : 계좌비밀번호를 입력하십시오.
            -302     : 타인 계좌를 사용할 수 없습니다.
            -303     : 경고-주문수량 200개 초과
            -304     : 제한-주문수량 400개 초과

        """
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

    def request_tick_info(self, subject_code, tick_unit, prevNext):

        self.set_input_value("종목코드", subject_code)
        self.set_input_value("시간단위", tick_unit)

        rqTag = "해외선물옵션틱차트조회" + "_" + subject_code + "_" + tick_unit

        self.comm_rq_data(rqTag, "opc10001", prevNext, subject.info[subject_code]['화면번호'])

    def request_min_info(self, subject_code, tick_unit, prevNext):

        self.set_input_value("종목코드", subject_code)
        self.set_input_value("시간단위", tick_unit)

        rqTag = "해외선물옵션분차트조회" + "_" + subject_code + "_" + tick_unit
        self.comm_rq_data(rqTag, "opc10002", prevNext, subject.info[subject_code]['화면번호'])

    def set_input_value(self, sID, sValue):
        """
        Tran 입력 값을 서버통신 전에 입력한다.

        :param sID: 아이템명
        :param sValue: 입력 값
        Ex) openApi.SetInputValue(“종목코드”, “000660”);
            openApi.SetInputValue(“계좌번호”, “5015123401”);
        """
        try:
            log.debug("set_input_value(), sID: %s, sValue: %s" % (sID, sValue))
            rq_thread.set_input_value(sID, sValue)
        except Exception as err:
            log.error(err)

    def comm_rq_data(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        """
        Tran을 서버로 송신한다.

        :param sRQName: 사용자구분 명
        :param sTrCode: Tran명 입력
        :param nPrevNext: 0:조회, 2:연속
        :param sScreenNo: 4자리의 화면번호
        Ex) openApi.CommRqData( “RQ_1”, “OPT00001”, 0, “0101”);
        :return:
        OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
        OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
        OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
        OP_ERR_NONE(0) – 정상처리
        """
        try:
            log.debug("comm_rq_data(), sRQName: %s, sTrCode: %s, nPrevNext: %s, sScreenNo: %s" % (sRQName, sTrCode, nPrevNext, sScreenNo))
            rq_thread.push(sRQName, sTrCode, nPrevNext, sScreenNo)
        except Exception as err:
            log.error(err)

    def quit(self):
        """ Quit the server """

        QApplication.quit()
        sys.exit()

    ####################################################

    # Control Event Handlers
    ####################################################

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, candle=None):
        """
        Tran 수신시 이벤트
        서버통신 후 데이터를 받은 시점을 알려준다.

        :param py: 화면번호
        :param sRQName: 사용자구분 명
        :param sTrCode: Tran 명
        :param sRecordName: Record 명
        :param sPreNext: 연속조회 유무
        :param nDataLength: 1.0.0.1 버전 이후 사용하지 않음.
        :param sErrorCode: 1.0.0.1 버전 이후 사용하지 않음.
        :param sMessage: 1.0.0.1 버전 이후 사용하지 않음.
        :param sSplmMsg: 1.0.0.1 버전 이후 사용하지 않음.
        """
        log.info("onReceiveTrData")

        try:
            pass
        except Exception as err:
            log.error(err)

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList, o_info=None):
        """
        체결데이터를 받은 시점을 알려준다.

        :param sGubun: 체결구분 - 0:주문체결통보, 1:잔고통보, 3:특이신호
        :param nItemCnt: 아이템갯수
        :param sFidList: 데이터리스트 - 데이터 구분은 ‘;’ 이다.
        """
        log.info("onReceiveChejanData")

        try:
            pass
        except Exception as err:
            log.error(err)

    def OnReceiveRealData(self, subject_code, sRealType, sRealData):
        """
        실시간 시세 이벤트
        실시간데이터를 받은 시점을 알려준다.

        :param subject_code: 종목코드
        :param sRealType: 리얼타입
        :param sRealData: 실시간 데이터전문
        """

    def OnEventConnect(self, nErrCode):
        """
        통신 연결 상태 변경시 이벤트

        :param nErrCode: 에러 코드 - 0이면 로그인 성공, 음수면 실패, 에러코드 참조
        """
        log.info("OnEventConnect received")

        if nErrCode == 0:
            log.info("로그인 성공")
            # 계좌번호 저장
            self.account = self.get_login_info("ACCNO")
            log.info("계좌번호 : " + self.account)

            if const.MODE is const.REAL:
                # 다이나믹 종목 정보 요청
                self.get_dynamic_subject_code()
                self.get_futures_deposit()
                self.get_my_deposit_info()

                # 종목 정보 로그 찍기
                log.info("참여 종목 : %s" % subject.info.values())


        else:
            c_time = "%02d%02d" % (time.localtime().tm_hour, time.localtime().tm_min)

            # 로그인 실패 로그 표시 및 에러코드별 에러내용 발송
            log.critical(rq_thread.parse_error_code(nErrCode))

            self.quit()
