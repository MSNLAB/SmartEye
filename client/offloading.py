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
def send_frame(url, frame, selected_model):

    # frame_shape = frame.shape
    msg_dict = {
        "selected_model": selected_model,
        # "frame_shape": frame_shape,
        "frame": frame
    }
    response = make_request.make_request(url, **msg_dict)
    # print(response)
    result = response.read().decode('utf-8')
    return result


# video file interface
def process_video_file(url, input_file):

        response = make_request.make_request(url)
        video = response.read().decode('utf-8')
        # if selected_model == "image classification":
        #     print(video)
        # else:
        #     save_file(video, input_file)