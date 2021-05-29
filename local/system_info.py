#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: system_infomation.py
@time: 2021/4/16 下午2:41
@desc:
'''

import psutil
from tools.read_config import read_config
import os
import datetime


class SysInfo:
    """
    storing the system information of local and server
    """
    def __init__(self, operation):

        #time = datetime.datetime.now()
        self.operation = operation + "_" + time.strftime('%a%b%d%H%M') + ".txt"
        # self.info_list = []
        self.cpu_usage = []
        self.bandwidth = []
        self.processing_delay = []
        self.memory_usage = []

    def append(self, total_service_delay, net_speed):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        info = (total_service_delay, net_speed, cpu_usage, memory_usage)
        self.info_list.append(info)

    def store(self):

        store_path = os.path.join(os.path.dirname(__file__), "../info_store/system_infomation")
        info_store_path = os.path.join(store_path, self.operation)
        info_title = ("total_service_delay", "net_speed", "cpu_usage", "memory_usage")
        with open(info_store_path, 'w+') as f:
            f.write(str(info_title) + '\n')
            for info in self.info_list:
                f.write(str(info) + '\n')


# import collections
#
# SysInfo = collections.namedtuple('SysInfo',['service_delay', 'net_speed', 'cpu_usage'])
if __name__ == "__main__":

    info = SysInfo("name")
    info.append("15")
    info.store()
