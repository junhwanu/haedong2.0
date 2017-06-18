# -*- coding: utf-8 -*-

import datetime

def get_today_date():
    today = datetime.date.today()
    year = str(today.year)
    month = str(today.month)
    if len(month) == 1: month = '0' + month

    day = str(today.day)
    if len(day) == 1: day = '0' + day

    return year + month + day