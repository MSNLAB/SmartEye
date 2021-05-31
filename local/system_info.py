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
    def __init__(self):
        now = datetime.datetime.now()
        self.file = "SysInfo" + "_" + now.strftime('%a%b%d%H%M') + ".log"
        self.infos = []
        self.cpu_usage = []
        self.bandwidth = []
        self.processing_delay = []
        self.memory_usage = []

    def append(self, start_time, processing_delay=None, bandwidth=None, cpu_usage=None, memory_usage=None):
        # cpu_usage = psutil.cpu_percent()
        # memory_usage = psutil.virtual_memory().percent
        assert start_time is not None, "start_time can't be None"
        assert (processing_delay is not None or
               bandwidth is not None or
               cpu_usage is not None or
               memory_usage is not None), "at least one parameter is not None"

        dict = {"time": start_time}

        if processing_delay is not None:
            dict["processing_delay"] = processing_delay
            self.processing_delay.append(processing_delay)
        if bandwidth is not None:
            dict["bandwidth"] = bandwidth
            self.bandwidth.append(bandwidth)
        if cpu_usage is not None:
            dict["cpu_usage"] = cpu_usage
            self.cpu_usage.append(cpu_usage)
        if memory_usage is not None:
            dict["memory_usage"] = memory_usage
            self.memory_usage.append(memory_usage)
        self.infos.append(dict)

    def store(self):

        store_path = os.path.join(os.path.dirname(__file__), "..\\info_store\\system_information")
        info_store_path = os.path.join(store_path, self.file)
        info_title = "time processing_delay bandwidth cpu_usage memory_usage"
        with open(info_store_path, 'w+') as f:
            for info in self.infos:
                f.write(str(info) + '\n')


# import collections
#
# SysInfo = collections.namedtuple('SysInfo',['service_delay', 'net_speed', 'cpu_usage'])
if __name__ == "__main__":

    # info = SysInfo("name")
    # info.append("15")
    # info.store()
    a = []
    print(a[-1])