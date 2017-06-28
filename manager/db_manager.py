# -*- coding: utf-8 -*-
import pymysql
from constant import *

curs = None
conn = None
is_connected = False

def connect():
    global curs, conn, is_connected
    conn = pymysql.connect(host=DB_SERVER_ADDR, user=DB_USER_ID, password=DB_USER_PWD, db=DB_NAME, charset=DB_CHARSET)
    curs = conn.cursor()
    is_connected = True

def disconnect():
    global curs, conn
    conn.close()

def exec_query(query, fetch_type = None, fetch_count = None, cursor_type = CURSOR_TUPLE):
    global curs, conn, is_connected

    if not is_connected: connect()

    if cursor_type == CURSOR_DICT:
        curs = conn.cursor(pymysql.cursors.DictCursor)
    elif cursor_type == CURSOR_TUPLE:
        curs = conn.cursor()

    result = curs.execute(query)
    conn.commit()

    if fetch_type == FETCH_ONE:
        return curs.fetchone()
    elif fetch_type == FETCH_ALL:
        return curs.fetchall()
    elif fetch_type == FETCH_MANY:
        return curs.fetchmany(fetch_count)
    else:
        return result

def exist_table(subject_code, date):
    query = "show tables in haedong like '%s_%s'" % (subject_code, date)

    row = exec_query(query, FETCH_ONE)

    if len(row) > 0: return True
    return False

def drop_table(table_name):
    query = "drop table %s" % table_name
    return exec_query(query)

def create_table(table_name):
    query = "create table %s select * from root_table" % table_name
    return exec_query(query)

def get_table(table_name):
    query = 'select date, price, working_day from %s' % table_name
    return exec_query(query, FETCH_ALL)

def get_table_list(subject_symbol, start_date, end_date):
    query = "show tables where substr(Tables_in_haedong, 1, 2) = '%s' and substr(Tables_in_haedong, (select char_length(Tables_in_haedong)) - 7, 8) between '%s' and '%s'" % (subject_symbol, start_date, end_date)
    return exec_query(query, FETCH_ALL)