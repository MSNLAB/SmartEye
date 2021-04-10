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
import time


video_path = '/home/wxz/Desktop/20200827153531.mp4'


def virtual_camera(video_name):
    """
    using pyvirtualcam package to send video frames to virtual camera
    :param video_name: video sent to virtual camera
    :return:
    """
    p = subprocess.call(['sudo', 'modprobe', 'v4l2loopback', 'devices=1'], stdout=subprocess.PIPE)
    # p.communicate()
    cap = cv2.VideoCapture(video_name)
    width, height, fps = get_video_info(video_name)
    # print(width, height, fps)
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
    # /home/wxz/Documents/video2edge
    name = os.path.basename(video_name).split(".")[0]
    json_file = "./" + name + ".json"
    # Does the reason that add the sudo command in the front result in program stop?
    cmd = ("ffprobe -print_format json -show_format -show_streams -i " +
           video_name + " > " + json_file)
    # subprocess.Popen create a subprocess to execute the cmd,
    # and the parent process don't wait the subprocess to finish
    # unless you use the wait or communicate function
    subprocess.call(cmd, shell=True, stderr=subprocess.PIPE)

    with open(json_file, 'r', encoding='utf8') as f:
        # info = f.read()
        # print(info)
        info = json.load(f)
    width = info["streams"][0]["width"]
    height = info["streams"][0]["height"]
    fps = info["streams"][0]["r_frame_rate"]
    return int(width), int(height), eval(fps)


if __name__ == "__main__":
    # virtual_camera(video_path)
    get_video_info(video_path)