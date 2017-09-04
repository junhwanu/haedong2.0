# -*- coding: utf-8 -*-

import os
import threading
import time

import pywinauto


class ClosePopup(threading.Thread):
    time = 0
    
    def __init__(self, time__):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.time = time__
    
    def run(self):
        time.sleep(self.time)
        app = pywinauto.Application().connect(process=os.getpid())
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title="OpenAPI-W"))
        dlg.Button0.click()
        return
