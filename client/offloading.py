#!/usr/bin/env python
# encoding: utf-8
"""
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: offloading.py
@time: 2021/4/16 下午2:37
@desc:
"""
import json

from tools import make_request
from client import preprocessing
from tools.transfer_files_tool import transfer_file_to_str, save_file


"""
transmission client interface: transmit data to server
"""


# picture interface
def send_frame(url, frame):

    response = make_request.make_request(url, frame)
    result = response.read().decode('utf-8')
    return result


# video file interface
def process_video_file(self, input_file):

    try:
        file_path = preprocessing.video_resolution_and_bitrate_adjust(input_file, **msg_dict)
    except:
        pass
    else:
        msg_dict = transfer_file_to_str(file_path)
        msg_dict["select_dict"] = selected_model
        response = make_request.make_request(video_file_url, **msg_dict)
        video = response.read().decode('utf-8')
        if selected_model == "image classification":
            print(video)
        else:
            save_file(video, input_file)