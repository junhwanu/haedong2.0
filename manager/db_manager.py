# -*- coding: utf-8 -*-
import pymysql
from constant.constant import *
from manager import __manager


class DBManager(__manager.ManagerClass):
    curs = None
    conn = None
    is_connected = False

    def __init__(self):
        super(DBManager, self).__init__()

    def connect(self):
        self.conn = pymysql.connect(host=DB_SERVER_ADDR, user=DB_USER_ID, password=DB_USER_PWD, db=DB_NAME, charset=DB_CHARSET)
        self.curs = self.conn.cursor()
        self.is_connected = True

    def disconnect(self):
        self.conn.close()

    def exec_query(self, query, fetch_type=None, fetch_count=None, cursor_type=CURSOR_TUPLE):
        if not self.is_connected:
            self.connect()

        if cursor_type == CURSOR_DICT:
            self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        elif cursor_type == CURSOR_TUPLE:
            self.curs = self.conn.cursor()

        result = self.curs.execute(query)
        self.conn.commit()

        if fetch_type == FETCH_ONE:
            return self.curs.fetchone()
        elif fetch_type == FETCH_ALL:
            return self.curs.fetchall()
        elif fetch_type == FETCH_MANY:
            return self.curs.fetchmany(fetch_count)
        else:
            return result

    def exist_table(self, subject_code, date):
        query = "show tables in haedong like '%s_%s'" % (subject_code, date)

        row = self.exec_query(query, FETCH_ONE)

        if len(row) > 0:
            return True

        return False

    def drop_table(self, table_name):
        query = "drop table %s" % table_name
        return self.exec_query(query)

    def create_table(self, table_name):
        query = 'create table %s select * from root_table' % table_name
        return self.exec_query(query)

    def get_table(self, table_name, start_date=None, end_date=None):
        if start_date is not None: query = 'select date, price, working_day from %s' % table_name
        else: query = "select date, price, working_day from %s where date >= timestamp('%s') and date = timestamp('%s')" % (table_name, start_date, end_date)

        return self.exec_query(query, FETCH_ALL)

    def get_table_list(self, subject_symbol):
        query = '''
        SELECT 
         table_name
        FROM 
         information_schema.tables
        WHERE 
         table_schema = DATABASE()
         and
         substr(table_name, 1, %s) = '%s'
        ''' %  (len(subject_symbol), subject_symbol)
        return list(self.exec_query(query, FETCH_ALL))

    def get_name(self):
        return str(self.__class__.__name__)

    def request_tick_candle(self, subject_code, tick_unit):
        query = '''
        select t1.id
             , t1.date
             , t1.high
             , t1.low
             , t2.price as open
             , t3.price as close
          from (
                select Floor((result.row-1) / '%s') + 1 as id
                     , min(date_format(result.date, '%%Y%%m%%d%%H%%i%%s')) as date
                     , max(result.id) as max_id
                     , min(result.id) as min_id
                     , max(result.price) as high
                     , min(result.price) as low
                  from (
                        select @rownum:=@rownum+1 as row
                             , id
                             , price
                             , date
                          from %s s1
                         inner join (
                                    select @rownum:=0
                                      from dual
                                    ) s2
                       ) result
                 group by Floor((result.row-1) / '%s')
               ) t1
         inner join %s t2
            on t1.min_id = t2.id
         inner join %s t3
            on t1.max_id = t3.id
        ;
        ''' % (tick_unit, subject_code, tick_unit, subject_code, subject_code)

        return self.exec_query(query, fetch_type=FETCH_ALL, cursor_type=CURSOR_DICT)

    def print_status(self):
        print(self.__getattribute__())

    def is_matched_table(self, table_name, c, d):
        query = '''
        select
            *
        from
            (select date(date) as s from %s order by date asc limit 1) R1
        inner join
            (select date(date) as e from %s order by date desc limit 1) R2
        ''' % (table_name, table_name)

        try:
            result = self.exec_query(query, fetch_type=FETCH_ONE, cursor_type=CURSOR_DICT)

            c = c[:4] + '-' + c[4:6] + '-' + c[6:]
            d = d[:4] + '-' + d[4:6] + '-' + d[6:]
            a = str(result['s'])
            b = str(result['e'])

        except Exception as err:
            print(err)
        if c <= a <= d <= b or c <= a <= b <= d or a <= c <= d <= b or a <= c <= b <= d: return True
        return False

if __name__ == '__main__':
    dbm = DBManager()
    result = dbm.request_tick_candle('GCJ17', 60)
    for rs in result:
        print(rs)