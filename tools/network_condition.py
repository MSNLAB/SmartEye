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
file_path = "test.zip"


def get_network_condition(url, file_path):
    # file_name = create_ramdom_file.create_file()
    test_str = transfer_file_to_str(file_path)
    response, service_delay = make_request.make_request(url, img_data=test_str)
    result = response.read().decode('utf-8')
    assert result != 'ok'
    net_speed = os.path.getsize(file_path) / (float(1024) * service_delay)
    return service_delay, net_speed
