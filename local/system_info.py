#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: system_information.py
@time: 2021/4/16 下午2:41
@desc:
'''
import time

import psutil
from tools.read_config import read_config
import os
import datetime


class SysInfo:
    """
    storing the system information of local and server
    """
    def __init__(self, input_file):
        pre_file = os.path.basename(input_file).split(".")[0]
        now = datetime.datetime.now()
        self.file = pre_file + "_" + now.strftime('%a%b%d%H%M') + ".txt"
        self.time_stamp = []
        self.cpu_usage = []
        self.bandwidth = []
        self.processing_delay = []
        self.memory_usage = []

    def append(self, start_time, processing_delay, bandwidth):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        self.time_stamp.append(start_time)
        self.processing_delay.append(processing_delay)
        self.bandwidth.append(bandwidth)
        self.cpu_usage.append(cpu_usage)
        self.memory_usage.append(memory_usage)

    def store(self):

        store_path = os.path.join(os.path.dirname(__file__), "..\\info_store\\system_information")
        info_store_path = os.path.join(store_path, self.file)
        info_title = "time processing_delay bandwidth cpu_usage memory_usage"
        with open(info_store_path, 'w+') as f:
            f.write(str(info_title) + '\n')
            for i in range(len(self.bandwidth)):
                content = (
                        str(self.time_stamp[i]) + " " +
                        str(self.processing_delay[i]) + " " +
                        str(self.bandwidth[i]) + " " +
                        str(self.cpu_usage[i]) + " " +
                        str(self.memory_usage[i])
                )
                f.write(content + '\n')


# import collections
#
# SysInfo = collections.namedtuple('SysInfo',['service_delay', 'net_speed', 'cpu_usage'])
if __name__ == "__main__":

    # info = SysInfo("name")
    # info.append("15")
    # info.store()
    a = []
    print(a[-1])