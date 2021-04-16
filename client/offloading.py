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
def process_picture(self, input_file):

    picture_path = preprocessing.image_size_adjust(input_file, image_size=msg_dict['image_size'])
    msg_dict = transfer_file_to_str(picture_path)
    msg_dict["selected_model"] = selected_model
    response = make_request.make_request(picture_url, **msg_dict)
    msg_str = response[0].read().decode('utf-8')
    if requirement_type[1] == "image classification":
        print(msg_str)
    else:
        msg_dict = json.loads(msg_str)
        save_file(picture_path, **msg_dict)


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