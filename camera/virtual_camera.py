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
# import numpy as np
import cv2
# from PIL import Image
import subprocess
# import os
# import json
# import time


class VirtualCamera:
    """
    This is a virtual camera
    """
    def __init__(self, video_name):
        """
        :param video_name: video sent to virtual camera
        """
        try:
            subprocess.call(['modprobe', 'v4l2loopback', 'device=1'], stdout=subprocess.PIPE, timeout=5)
        except Exception as err:
            print("error:", err)
        self.cap = cv2.VideoCapture(video_name)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def send_video_to_virtual_camera(self):
        """
        using pyvirtualcam package to send video frames to virtual camera
        :return:
        """
        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as cam:
            while self.cap.isOpened():
                _, frame = self.cap.read()
                if frame is None:
                    break
                cam.send(frame)
                cam.sleep_until_next_frame()
        self.cap.release()


if __name__ == "__main__":
    # virtual_camera(video_path)
    # get_video_info(video_path)
    video_path = '/home/wxz/Desktop/20200827153531.mp4'
    vircam = VirtualCamera(video_path)
    vircam.send_video_to_virtual_camera()
