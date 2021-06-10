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
import os
import datetime


class SysInfo:
    """Storing the system information of local and server

    This is a system information class. it Stores every information of system execution,
    such as cpu usage, process time.
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
        """Add system info into list respectively.

        :param start_time: the time of collecting system information.
        :param processing_delay: the time of processing image data.
        :param bandwidth: current bandwidth.
        :param cpu_usage: cpu usage.
        :param memory_usage: memory usage.
         :return: None.
        """
        assert start_time is not None, "start_time can't be None"
        assert (processing_delay is not None or
               bandwidth is not None or
               cpu_usage is not None or
               memory_usage is not None), "at least one parameter is not None"

        dict = {"time": start_time}

        if processing_delay is not None:
            dict["processing_delay"] = processing_delay
            self.processing_delay += [processing_delay]
        if bandwidth is not None:
            dict["bandwidth"] = bandwidth
            self.bandwidth += [bandwidth]
        if cpu_usage is not None:
            dict["cpu_usage"] = cpu_usage
            self.cpu_usage += [cpu_usage]
        if memory_usage is not None:
            dict["memory_usage"] = memory_usage
            self.memory_usage += [memory_usage]

        self.infos += [dict]

    def store(self):
        """Store the system information into a file.

        :return: None
        """
        store_path = os.path.join(os.path.dirname(__file__), "..\\info_store\\system_information")
        info_store_path = os.path.join(store_path, self.file)
        info_title = "time processing_delay bandwidth cpu_usage memory_usage"
        with open(info_store_path, 'w+') as f:
            for info in self.infos:
                f.write(str(info) + '\n')


if __name__ == "__main__":

    a = []
    print(a[-1])
