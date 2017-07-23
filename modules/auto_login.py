# -*- coding: utf-8 -*-

import threading
import time
import psutil
import pywinauto
import configparser
import os
import pyautogui
import cv2
from PIL import Image


class Login(threading.Thread):
    LOGIN_PNAME = ["kfstarter.exe", "KFStarter.exe"]
    PYTHON_PNAME = "python.exe"

    REAL_INVEST = False
    AUTO_LOGIN = True

    USER_ID = 'id'
    USER_PASSWD = 'passwd'
    AUTH_PASSWD = 'passwd'

    AUTO_WRITE_PASSWD = True
    ACCOUNT_PASSWD = '0000'

    MODULE_PATH = os.path.dirname(os.path.abspath(__file__).replace('\\', '/'))

    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

        # 사용자 계정 정보 Config 읽기
        config = configparser.RawConfigParser()
        config.read(self.MODULE_PATH + '/../config/user.cfg')

        # config file searching
        if config.has_section('AUTO_LOGIN_CONFIG'):

            if config.BOOLEAN_STATES.get(config.get('AUTO_LOGIN_CONFIG', 'AUTO_LOGIN_ENABLE')):
                self.AUTO_LOGIN = True
                self.USER_ID = config.get('AUTO_LOGIN_CONFIG', 'USER_ID')
                self.USER_PASSWD = config.get('AUTO_LOGIN_CONFIG', 'USER_PASSWD')

                # 실제 투자 / 모의투자
                if config.BOOLEAN_STATES.get(config.get('AUTO_LOGIN_CONFIG', 'REAL_INVEST_FLAG')):
                    self.REAL_INVEST = True
                    self.AUTH_PASSWD = config.get('AUTO_LOGIN_CONFIG', 'AUTH_PASSWD')
                else:
                    self.REAL_INVEST = False

                if config.BOOLEAN_STATES.get(config.get('AUTO_ACCOUNT_PASSWD_CONFIG', 'AUTO_ACCOUNT_PASSWD_ENABLE')):
                    self.AUTO_WRITE_PASSWD = True
                    self.ACCOUNT_PASSWD = config.get('AUTO_ACCOUNT_PASSWD_CONFIG', 'ACCOUNT_PASSWD')
                else:
                    self.AUTO_WRITE_PASSWD = False

            else:
                self.AUTO_LOGIN = False

        else:
            print('Auto Login Config File을 찾을 수 없습니다.')
            self.AUTO_LOGIN = False
            time.sleep(1)

    def auto_login(self):
        if self.REAL_INVEST:
            print("실제 투자용 자동 로그인")
        else:
            print("모의 투자용 자동 로그인")

        time.sleep(3)

        looping_flag = True
        login_pid = 0

        while looping_flag:
            for proc in psutil.process_iter():
                if proc.name() in self.LOGIN_PNAME:
                    login_pid = proc.pid
                    print('로그인 프로그램 pid(%d)' % login_pid)
                    looping_flag = False

            if looping_flag:
                print("로그인 프로그램을 찾는 중입니다.")
                time.sleep(5)

        app = pywinauto.Application().connect(process=login_pid)

        title = "영웅문W Login"
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

        try:
            dlg.Edit1.SetFocus()
        except pywinauto.findwindows.ElementNotFoundError as err:
            time.sleep(3)
            print("로그인 윈도우를 찾지 못했습니다. 5초후 재시도")

        계정입력 = dlg.Edit1
        계정입력.SetFocus()
        계정입력.TypeKeys(self.USER_ID)
        print('키움 사용자 ID(%s)' % self.USER_ID)

        비밀번호입력 = dlg.Edit2
        비밀번호입력.SetFocus()
        비밀번호입력.TypeKeys(self.USER_PASSWD)
        print('키움 사용자 PASSWORD(%s)' % self.USER_PASSWD)

        # 모의투자
        if self.REAL_INVEST:
            공인인증서비밀번호 = dlg.Edit3
            공인인증서비밀번호.SetFocus()
            공인인증서비밀번호.TypeKeys(self.AUTH_PASSWD)
            print('공인인증서 PASSWORD(%s)' % self.AUTH_PASSWD)

        로그인버튼 = dlg.Button0
        로그인버튼.Click()

    def auto_write_passwd(self):
        화면x, 화면y = pyautogui.size()
        아이콘 = Image.open(self.MODULE_PATH + '/../resource/kf.png')

        while True:
            print('트레이 아이콘을 찾는 중입니다.')
            아이콘위치 = pyautogui.locateCenterOnScreen(아이콘, region=(화면x - 400, 화면y - 100, 400, 100), confidence=.5)

            if 아이콘위치:
                print('트레이 아이콘을 찾았습니다.')
                print(아이콘위치)
                x, y = 아이콘위치
                print(x, y)
                pyautogui.click(x, y, button='right')
                break

        time.sleep(2)
        # 등록 버튼 누르기
        print('등록버튼 누르기')
        pyautogui.moveRel(10, -35)
        pyautogui.click()

        time.sleep(2)

        looping_flag = True
        kfopcom_pid = 0

        while looping_flag:
            for proc in psutil.process_iter():
                if proc.name() in self.PYTHON_PNAME:
                    kfopcom_pid = proc.pid
                    print('거래 프로그램 pid(%d)' % kfopcom_pid)
                    looping_flag = False

            if looping_flag:
                print("거래 프로그램을 찾는 중입니다.")
                time.sleep(5)

        time.sleep(5)

        app = pywinauto.Application().connect(process=kfopcom_pid)

        title = "계좌번호관리"
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))
        # app.window_().print_control_identifiers()

        비밀번호수정 = dlg.Edit1
        비밀번호수정.SetFocus()
        비밀번호수정.Click()
        비밀번호수정.TypeKeys(self.ACCOUNT_PASSWD)
        print(self.ACCOUNT_PASSWD)

        time.sleep(0.5)

        일괄저장버튼 = dlg.Button3
        일괄저장버튼.Click()

        time.sleep(0.5)

        닫기버튼 = dlg.Button2
        닫기버튼.Click()

        return

    def run(self):
        if self.AUTO_LOGIN is False:
            print("자동 로그인을 사용하지 않습니다.")
            return

        self.auto_login()

        time.sleep(15)

        # 자동 비밀번호 입력
        if self.AUTO_WRITE_PASSWD is False:
            print('자동 비밀번호 입력을 사용하지 않습니다.')
            return

        self.auto_write_passwd()

        print("Auto Login Thread 종료")
        # self.account_password_setup()


if __name__ == '__main__':
    login = Login()
    login.start()