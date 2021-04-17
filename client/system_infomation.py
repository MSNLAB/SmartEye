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


# class SysInfo:
#     """
#     storing the system information of client and server
#     """
#     def __init__(self):
#         self.service_delay = 0
#         self.net_speed = 0
#         self.cpu_usage = 0
#         pass
import collections

SysInfo = collections.namedtuple('SysInfo',['service_delay', 'net_speed', 'cpu_usage'])

