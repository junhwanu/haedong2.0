# -*- coding: utf-8 -*-
import configparser
import os

import psutil
import pywinauto

from modules.__module import ModuleClass


class Destroy_python(ModuleClass):
    my_pid = 0
    
    MODULE_PATH = os.path.dirname(os.path.abspath(__file__).replace('\\', '/'))
    enable_modules = False

    def __init__(self):
        super(Destroy_python, self).__init__()
        self.my_pid = os.getpid()
        
        config = configparser.RawConfigParser()
        config.read(self.MODULE_PATH + '/../config/user.cfg')
        
        if config.has_section('DESTROY_PYTHON_CONFIG'):
            if config.BOOLEAN_STATES.get(config.get('DESTROY_PYTHON_CONFIG', 'DESTROY_PYTHON_ENABLE')):
                self.enable_modules = True
                
            else:
                self.enable_modules = False
                
        else:
            self.log.info("Auto Login Config File을 찾을 수 없습니다.")
            self.log.info("Python 종료 기능을 사용 할 수 없습니다.")
            self.enable_modules = False
                
        self.destroy_p()
        
    def destroy_p(self):
        if self.enable_modules is True:
            self.log.info("Python 종료기능을 사용합니다.")
        else :
            self.log.info("Python 종료기능을 사용하지 않습니다.")
            return
            
        print("my pid = " + str(self.my_pid))
        for proc in psutil.process_iter():
            if proc.name() in ["python.exe"]:
                print(proc.name() + "   "  + str(proc.pid))
                
                if self.my_pid != proc.pid:
                    print("other pid = " + str(proc.pid))
                    app = pywinauto.Application().connect(process=proc.pid)
                    app.kill()
                    self.destroy_p()
        
    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        self.log.info(self.__getattribute__())