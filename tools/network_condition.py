#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: network_condition.py
@time: 2021/4/16 下午1:33
@desc:
'''
import os

from tools import make_request
from tools.transfer_files_tool import transfer_file_to_str
from tools.read_config import read_config


file_path = read_config("test-file-path", "test_path")


def get_network_condition(url):
    # file_name = create_ramdom_file.create_file()
    test_dict = transfer_file_to_str(file_path)
    result_dict, total_service_delay, time_to_transfer_server = make_request.make_request(url, **test_dict)
    assert result_dict["result"] == 'ok'
    net_speed = os.path.getsize(file_path) / time_to_transfer_server
    return total_service_delay, net_speed
