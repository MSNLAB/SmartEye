#!/usr/bin/env python
# encoding: utf-8
'''
@author: Xuezhi Wang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: virtual_camera.py
@time: 2021/4/9 下午3:19
@desc:
'''
import pyvirtualcam
import numpy as np
import cv2
from PIL import Image
import subprocess
import os
import json


subprocess.Popen(['sudo', 'modprobe', 'v4l2loopback', 'devices=1'], stdout=subprocess.PIPE)
video_path = '/home/wxz/Desktop/20200827153531.mp4'


def virtual_camera(video_name):
    """
    using pyvirtualcam package to send video frames to virtual camera
    :param video_name: video sent to virtual camera
    :return:
    """

    cap = cv2.VideoCapture(video_name)
    width, height, fps = get_video_info(video_name)
    with pyvirtualcam.Camera(width=width, height=height, fps=fps) as cam:

        while cap.isOpened():
            _, frame = cap.read()
            if frame is None:
                break
            cam.send(frame)
            cam.sleep_until_next_frame()

    cap.release()


def read_from_camera():
    cap = cv2.VideoCapture(0)


def get_video_info(video_name):
    """
    get width, height, frames information of video
    :param video_name: video
    :return:
    """
    name = os.path.basename(video_name).split(".")[0]
    json_file = "./" + name + ".json"
    cmd = ("ffprobe -print_format json -show_format -show_streams -i " +
           video_name + ">>" + json_file)
    print(cmd)
    subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    with open(json_file, 'r') as f:
        info = json.load(f)
        width = info["streams"]["width"]
        height = info["streams"]["height"]
        frames = info["streams"]["r_frame_rate"]
    # out = info.communicate()
    # print(out)


if __name__ == "__main__":
    get_video_info(video_path)