# -*- coding: utf8 -*-

import socket
import time
import datetime
import sys


# Headong과 독립적인 Module
# 호스트, 포트와 버퍼 사이즈를 지정
TARGET_HOST = '211.253.11.13'
HEALTH_PORT = 56789
BUFF_SIZE = 1024

CHECK_INTERVAL = 5


class HealthChecker:

    def __init__(self):
        self.bind_ip = ''

        print('Write Target IP address (default=localhost) : ')
        self.server_ip = input()

        if self.server_ip.__len__() < 5:
            self.server_ip = TARGET_HOST

        print("Target IP : " + self.server_ip)

        self.server_ip = TARGET_HOST

    def notify(self):
        print("Server die (Add code for notification to you)!")
        # Add code for notification to you

    def single_check(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.bind_ip, 0))

        try:
            sock.connect((self.server_ip, HEALTH_PORT))

            # Send Echo
            message = datetime.datetime.now()
            send_buff = bytes(str(message), encoding="utf-8")
            sock.send(send_buff)

            # Receive Echo
            recv_buff = sock.recv(BUFF_SIZE)
            recv_message = str(recv_buff, encoding="utf-8")
            print("checked : {0}".format(recv_message))
            return 0

        except Exception as err:
            print("Exception ({0})".format(err))
            sock.close()
            return -1

        finally:
            sock.close()

    def looping_check(self):
        while True:
            result = self.single_check()
            if result == 0:
                time.sleep(CHECK_INTERVAL)
                continue
            else:
                self.notify()
                sleep_in_down = 10
                time.sleep(sleep_in_down)
                continue


if __name__ == '__main__':
    checker = HealthChecker()
    checker.looping_check()