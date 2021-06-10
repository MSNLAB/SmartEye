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
from tools import make_request
from tools.transfer_files_tool import transfer_array_and_str


def send_frame(url, frame, selected_model):
    """Send the image frame to the transfer server.

    Send the image frame to the transfer server, and get the result of server.
    At the same time, calculate the time of total processing and arrive transfer server delay.

    :param url: transfer server's url
    :param frame: image frame to send to server
    :param selected_model: model name to send to server
    :return: result_dict: result dict returned from server
             start_time: the start time of calculating the time
             processing_delay: total processing time
             arrive_transfer_server_time: the delay between client and transfer server
    """
    frame_shape = frame.shape
    img_str = transfer_array_and_str(frame, "up")
    msg_dict = {
        "selected_model": selected_model,
        "frame_shape": frame_shape,
        "frame": img_str
    }
    try:
        result_dict, start_time, processing_delay, arrive_transfer_server_time = make_request.make_request(url, **msg_dict)
    except:
        print("servers return nothing ")
    else:
        return result_dict, start_time,  processing_delay, arrive_transfer_server_time


# video file interface
def process_video_file(url, input_file):

        response = make_request.make_request(url)
        video = response.read().decode('utf-8')
        # if selected_model == "image classification":
        #     print(video)
        # else:
        #     save_file(video, input_file)
