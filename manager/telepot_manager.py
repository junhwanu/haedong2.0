# -*- coding: utf-8 -*-
import telepot
from __manager import ManagerClass
import singleton

# Singleton class --> there is only one log manager


class TelepotManager(metaclass=singleton.SingletonInstane):
    TOKEN = '339704326:AAEXoMPlPLsuA5uMqdCUF-Wq5QMyKqNsgYo'
    id_list = []

    def __init__(self):
        super(TelepotManager, self).__init__()

    def set_account(self, account):
        self.id_list = []

        if account is None:
            self.id_list.append(285446312) # 진모
            self.id_list.append(330172669) # 희준
            self.id_list.append(377943640) # 남용
        elif account == '5107243872' or account == '7003919272':
            self.id_list.append(330172669) # 희준
        elif account == '5105855972':
            self.id_list.append(285446312) # 진모
        elif account == '51115392':
            self.id_list.append(377943640) # 남용

    def send_message(self, msg):
        if len(self.id_list) == 0:
            return

        bot = telepot.Bot(self.TOKEN)
        for id_ in self.id_list:
            bot.sendMessage(id_, msg)

    def get_name(self):
        return str(self.__class__.__name__)

    def print_status(self):
        print(self.__getattribute__())
