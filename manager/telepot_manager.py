# -*- coding: utf-8 -*-
import telepot

TOKEN = '339704326:AAEXoMPlPLsuA5uMqdCUF-Wq5QMyKqNsgYo'

id_list = []

def init(account):
    if account == None:
        id_list.append(285446312) # 진모
        id_list.append(330172669) # 희준
        id_list.append(377943640) # 남용
    elif account == '5107243872' or account == '7003919272':
        id_list.append(330172669) # 희준
    elif account == '5105855972':
        id_list.append(285446312) # 진모
    elif account =='51115392':
        id_list.append(377943640) # 남용

def sendMessage(msg):
    if len(id_list) == 0: return

    bot = telepot.Bot(TOKEN)

    for id in id_list:
        bot.sendMessage(id, msg)
