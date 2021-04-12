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


class VirtualCamera:
    """
    This is a virtual camera
    """
    def __init__(self, video_name):
        """
        :param video_name: video sent to virtual camera
        """
        try:
            subprocess.call(['modprobe', 'v4l2loopback'], stdout=subprocess.PIPE, timeout=5)
        except Exception as err:
            print("error:", err)
        self.video_name = video_name
        self.width, self.height, self.fps = self.get_video_info(self.video_name)

    def send_video_to_virtual_camera(self):
        """
        using pyvirtualcam package to send video frames to virtual camera
        :return:
        """
        cap = cv2.VideoCapture(self.video_name)
        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as cam:
            while cap.isOpened():
                _, frame = cap.read()
                if frame is None:
                    break
                cam.send(frame)
                cam.sleep_until_next_frame()
        cap.release()

    def get_video_info(self, video_name):
        """
        get width, height, fps information of video
        :param video_name: video
        :return:
        """
        name = os.path.basename(video_name).split(".")[0]
        json_file = "./" + name + ".json"
        # Is the reason that add the sudo command in the front result in program stop?
        cmd = ("ffprobe -print_format json -show_format -show_streams -i " +
               video_name + " > " + json_file)
        # subprocess.Popen create a subprocess to execute the cmd,
        # and the parent process don't wait the subprocess to finish
        # unless you use the wait or communicate function
        subprocess.call(cmd, shell=True, stderr=subprocess.PIPE)

        with open(json_file, 'r', encoding='utf8') as f:
            info = json.load(f)

        width = info["streams"][0]["width"]
        height = info["streams"][0]["height"]
        fps = info["streams"][0]["r_frame_rate"]
        return int(width), int(height), eval(fps)


if __name__ == "__main__":
    # virtual_camera(video_path)
    # get_video_info(video_path)
    video_path = '/home/wxz/Desktop/20200827153531.mp4'
    vircam = VirtualCamera(video_path)
    vircam.send_video_to_virtual_camera()
