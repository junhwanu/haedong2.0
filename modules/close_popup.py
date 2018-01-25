# -*- coding: utf-8 -*-

import os
import threading
import time

import pywinauto
from pywinauto.findwindows import ElementNotFoundError
from modules import __module


class ClosePopup(__module.ModuleClass, threading.Thread):
    time = 0
    
    def __init__(self, time__):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.time = time__
    
    def run(self):
        time.sleep(self.time)
        try:
            app = pywinauto.Application().connect(process=os.getpid())
            dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title="OpenAPI-W"))
            dlg.Button0.click()
            
        except ElementNotFoundError:
            return
        
        return

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        self.log.info(self.__getattribute__())
