#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@desc:
'''
import os
import time
import psutil
from loguru import logger


def get_local_utilization():
    """Get the CPU usage and memory usage"""
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage


class SysInfo:
    """Storing the system information of local and server

    This is a system information class. it Stores every information of system execution,
    such as cpu usage, process time.
    """
    def __init__(self):
        self.info = []
        self.cpu_usage = []
        self.memory_usage = []
        self.bandwidth = []
        self.processing_delay = []

    def update_local_utilization(self):
        """Update local utilization including cpu usage and memory usage"""
        cpu_usage, memory_usage = get_local_utilization()
        self.cpu_usage.append(cpu_usage)
        self.memory_usage.append(memory_usage)

    def append(self, start_time, processing_delay=None, bandwidth=None, cpu_usage=None, memory_usage=None):
        """Add system info into list respectively.

        :param start_time: the time of collecting system information.
        :param processing_delay: the time of processing image data.
        :param bandwidth: current bandwidth.
        :param cpu_usage: cpu usage.
        :param memory_usage: memory usage.
         :return: None.
        """
        try:
            assert start_time is not None, "start_time can't be None"
            assert (processing_delay is not None or
                   bandwidth is not None or
                   cpu_usage is not None or
                   memory_usage is not None), "at least one parameter is not None"
        except AssertionError as err:
            logger.exception("System information append error: ", err)

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


if __name__ == "__main__":
    a = []
    print(a[-1])
