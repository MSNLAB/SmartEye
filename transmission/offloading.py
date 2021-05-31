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
import base64
import json

from tools import make_request
from local import preprocessor
from tools.transfer_files_tool import transfer_file_to_str, save_file, transfer_array_and_str

"""
transmission local interface: transmit data to server
"""


# picture interface
def send_frame(url, frame, selected_model):

    frame_shape = frame.shape
    img_str = transfer_array_and_str(frame, "up")
    msg_dict = {
        "selected_model": selected_model,
        "frame_shape": frame_shape,
        "frame": img_str
    }
    result_dict, start_time, total_service_delay, arrive_transfer_server_time = make_request.make_request(url, **msg_dict)
    # result = response.read().decode('utf-8')

    return result_dict, start_time,  total_service_delay, arrive_transfer_server_time


# video file interface
def process_video_file(url, input_file):

        response = make_request.make_request(url)
        video = response.read().decode('utf-8')
        # if selected_model == "image classification":
        #     print(video)
        # else:
        #     save_file(video, input_file)
