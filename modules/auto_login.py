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
from modules import __module


class Login(__module.ModuleClass, threading.Thread):
    REAL_INVEST = False
    AUTO_LOGIN = True

    USER_ID = 'id'
    USER_PASSWD = 'passwd'
    AUTH_PASSWD = 'passwd'

    AUTO_WRITE_PASSWD = True
    ACCOUNT_PASSWD = '0000'

    MODULE_PATH = os.path.dirname(os.path.abspath(__file__).replace('\\', '/'))

    def __init__(self):
        super(Login, self).__init__()
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
            self.log.info("Auto Login Config File을 찾을 수 없습니다.")
            self.log.info('자동 로그인 기능을 사용 할 수 없습니다.')
            self.AUTO_LOGIN = False

    def auto_login(self):
        if self.REAL_INVEST:
            self.log.info("실제 투자용 모드")
        else:
            self.log.info("모의 투자용 모드")

        dlg = None

        for proc in psutil.process_iter():
            if proc.name() in ["kfstarter.exe", "KFStarter.exe"]:
                login_pid = proc.pid
                self.log.info("로그인 프로그램(" + str(proc) + ")")
                app = pywinauto.Application().connect(process=login_pid)
                dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title="영웅문W Login"))

                try:
                    dlg.Edit1.SetFocus()
                    break
                except pywinauto.findwindows.ElementNotFoundError as err:
                    self.log.info(str(proc) + "에서 로그인 윈도우를 찾지 못했습니다")
                    dlg = None

        try:
            계정입력 = dlg.Edit1
            계정입력.SetFocus()
            계정입력.TypeKeys(self.USER_ID)
            self.log.info("키움 사용자 ID(" + str(self.USER_ID) + ")")

            비밀번호입력 = dlg.Edit2
            비밀번호입력.SetFocus()
            비밀번호입력.TypeKeys(self.USER_PASSWD)
            self.log.info("키움 사용자 PASSWORD(" + str(self.USER_PASSWD) + ")")

            # 모의투자
            if self.REAL_INVEST:
                공인인증서비밀번호 = dlg.Edit3
                공인인증서비밀번호.SetFocus()
                공인인증서비밀번호.TypeKeys(self.AUTH_PASSWD)
                self.log.info("공인인증서 PASSWORD(" + str(self.AUTH_PASSWD) + ")")

            로그인버튼 = dlg.Button0
            로그인버튼.Click()

        except pywinauto.findwindows.ElementNotFoundError as err:
            self.log.info("로그인 윈도우를 찾지 못했습니다")
            return False

        return True

    def remove_dummy_icon(self):
        화면x, 화면y = pyautogui.size()
        아이콘 = Image.open(self.MODULE_PATH + '/../resource/kf.png')

        while True:
            아이콘위치 = pyautogui.locateCenterOnScreen(아이콘, region=(화면x - 400, 화면y - 100, 400, 100), confidence=.5)

            if 아이콘위치:
                self.log.info("더미 아이콘 제거." + str(아이콘위치))
                x, y = 아이콘위치
                pyautogui.moveTo(x, y)

            else:
                break

        self.log.info("더미 아이콘이 없습니다.")
        pyautogui.moveTo(화면x/2, 화면y/2)

    def auto_write_passwd(self):
        화면x, 화면y = pyautogui.size()
        아이콘 = Image.open(self.MODULE_PATH + '/../resource/kf.png')

        while True:
            self.log.info("트레이 아이콘을 찾는 중입니다.")
            아이콘위치 = pyautogui.locateCenterOnScreen(아이콘, region=(화면x - 400, 화면y - 100, 400, 100), confidence=.5)

            if 아이콘위치:
                self.log.info("트레이 아이콘을 찾았습니다." + str(아이콘위치))
                x, y = 아이콘위치
                pyautogui.click(x, y, button='right')
                break

            time.sleep(2)

        # 등록 버튼 누르기
        self.log.info("등록버튼 누르기")
        pyautogui.moveRel(10, -35)
        pyautogui.click()

        dlg = None

        for proc in psutil.process_iter():
            if proc.name() in ["python.exe"]:
                kfopcom_pid = proc.pid
                self.log.info("거래 프로그램(" + str(proc) + ")")
                app = pywinauto.Application().connect(process=kfopcom_pid)
                dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title="계좌번호관리"))

                try:
                    dlg.Edit1.SetFocus()
                    break
                except pywinauto.findwindows.ElementNotFoundError as err:
                    self.log.info(str(proc) + "에서 윈도우를 찾지 못했습니다.")
                    dlg = None

        try:
            비밀번호수정 = dlg.Edit1
            비밀번호수정.SetFocus()
            비밀번호수정.Click()
            비밀번호수정.TypeKeys(self.ACCOUNT_PASSWD)
            # self.log.info(self.ACCOUNT_PASSWD)

            일괄저장버튼 = dlg.Button3
            일괄저장버튼.Click()

            닫기버튼 = dlg.Button2
            닫기버튼.Click()

        except pywinauto.findwindows.ElementNotFoundError:
            self.log.info("거래 비밀번호 윈도우를 찾지 못했습니다")
            return False
        except AttributeError as err:
            self.log.info("거래 비밀번호 윈도우를 찾지 못했습니다")
            return False

        return True

    def run(self):
        if self.AUTO_LOGIN is False:
            self.log.info("자동 로그인을 사용하지 않습니다.")
            return

        self.log.info("자동 로그인 사용합니다.")
        while self.auto_login() is False:
            self.log.info("자동 로그인 실패! 5초 후 다시 시도합니다.")
            time.sleep(5)
            continue

        self.log.info("로그인 화면 정상처리 완료되었습니다.")

        # 자동 비밀번호 입력
        if self.AUTO_WRITE_PASSWD is False:
            self.log.info("자동 비밀번호 입력을 사용하지 않습니다.")
            return

        self.log.info("자동 비밀번호 입력 사용합니다.")
        self.log.info("더미 아이콘을 제거합니다.")
        self.remove_dummy_icon()
        time.sleep(5)

        while self.auto_write_passwd() is False:
            self.log.info("자동 비밀번호 입력 실패! 5초 후 다시 시도합니다.")
            time.sleep(5)
            continue

        self.log.info("비밀번호 입력 화면 정상 처리!")
        self.log.info("Auto Login 정상 종료")

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        self.log.info(self.__getattribute__())

if __name__ == '__main__':
    login = Login()
    login.start()