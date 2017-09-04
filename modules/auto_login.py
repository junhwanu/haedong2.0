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
                except pywinauto.findwindows.ElementNotFoundError:
                    self.log.info(str(proc) + "에서 로그인 윈도우를 찾지 못했습니다")
                    dlg = None

        try:
            dlg.Edit1.set_focus()
            dlg.Edit1.send_keystrokes(self.USER_ID)
            self.log.info("키움 사용자 ID(" + str(self.USER_ID) + ")")
            
            dlg.Edit2.set_focus()
            dlg.Edit2.send_keystrokes(self.USER_PASSWD)
            self.log.info("키움 사용자 PASSWORD(" + str(self.USER_PASSWD) + ")")
            
            # 모의투자
            if self.REAL_INVEST:
                dlg.Edit3.send_keystrokes(self.AUTH_PASSWD)
                self.log.info("공인인증서 PASSWORD(" + str(self.AUTH_PASSWD) + ")")

            time.sleep(1)
            dlg.Button0.Click()

        except pywinauto.findwindows.ElementNotFoundError:
            self.log.info("로그인 윈도우를 찾지 못했습니다")
            return False

        return True

    def remove_dummy_icon(self):
        x, y = pyautogui.size()
        icon = Image.open(self.MODULE_PATH + '/../resource/kf.png')

        while True:
            icon_position = pyautogui.locateCenterOnScreen(icon, region=(x - 400, y - 100, 400, 100), confidence=.5)

            if icon_position:
                self.log.info("더미 아이콘 제거." + str(icon_position))
                x, y = icon_position
                pyautogui.moveTo(x, y)
                time.sleep(0.5)
                
            else:
                break

        self.log.info("더미 아이콘이 없습니다.")
        pyautogui.moveTo(x/2, y/2)

    def auto_write_passwd(self):
        x, y = pyautogui.size()
        icon = Image.open(self.MODULE_PATH + '/../resource/kf.png')

        while True:
            self.log.info("트레이 아이콘을 찾는 중입니다.")
            icon_position = pyautogui.locateCenterOnScreen(icon, region=(x - 400, y - 100, 400, 100), confidence=.5)
            time.sleep(2)
            
            if icon_position:
                self.log.info("트레이 아이콘을 찾았습니다." + str(icon_position))
                x, y = icon_position
                break
            
        # 등록 버튼 누르기
        pyautogui.click(x, y, button='right')
        time.sleep(.1)
        pyautogui.click(x+10, y-35, button='left')
        self.log.info("등록버튼 누르기 완료")

        time.sleep(1)
        
        app = pywinauto.Application().connect(process=os.getpid())
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title="계좌번호관리"))
        
        try:
            dlg.Edit1.Click()
            time.sleep(.5)
            dlg.Edit1.send_keystrokes(self.ACCOUNT_PASSWD)
            time.sleep(.5)
            dlg.Button3.Click()
            time.sleep(.5)
            dlg.Button2.Click()

        except pywinauto.findwindows.ElementNotFoundError:
            self.log.info("거래 비밀번호 윈도우를 찾지 못했습니다")
            return False
        
        except AttributeError:
            self.log.info("거래 비밀번호 윈도우를 찾지 못했습니다")
            return False

        return True

    def run(self):
        self.log.info("자동 비밀번호 입력 사용합니다.")
        self.log.info("더미 아이콘을 제거합니다.")
        self.remove_dummy_icon()
        
        if self.AUTO_LOGIN is False:
            self.log.info("자동 로그인을 사용하지 않습니다.")
            return

        self.log.info("자동 로그인 사용합니다.")
        while self.auto_login() is False:
            self.log.info("자동 로그인 실패! 5초 후 다시 시도합니다.")
            time.sleep(5)
            continue

        self.log.info("로그인 화면 정상처리 완료되었습니다.")
        
        time.sleep(5)

        # 자동 비밀번호 입력
        if self.AUTO_WRITE_PASSWD is False:
            self.log.info("자동 비밀번호 입력을 사용하지 않습니다.")
            return

        time.sleep(5)

        while self.auto_write_passwd() is False:
            self.log.info("자동 비밀번호 입력 실패! 5초 후 다시 시도합니다.")
            time.sleep(5)
            continue

        self.log.info("비밀번호 입력 화면 정상 처리!")
        self.log.info("Auto Login 정상 종료")
        return
    
    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        self.log.info(self.__getattribute__())
        

if __name__ == '__main__':
    login = Login()
    login.start()