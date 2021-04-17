#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: local_store.py
@time: 2021/4/16 下午2:25
@desc:
'''
import cv2
import datetime


class LocalStore:
    """
    according to the requirements, LocalStore stores the input video frame
    as image or video in local directory
    """

    def __init__(self):
        time = datetime.datetime.now()
        video_name = "/home/wxz/" + time.date() + "_" + time.hour + ".mp4"
        self.out = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480)
        )

    def store_image(self, frame):
        """
        store frame as image
        :param frame: image which will be stored, type numpy.narray
        :return:
        """
        try:
            cv2.SaveImage("out.png", frame)
        except Exception as err:
            print("save image fail:", err)

    def store_video(self, frame):
        """
        store frame as image
        :param frame: image which will be stored, type numpy.narray
        :return:
        """
        try:
            self.out.write(frame)
        except Exception as err:
            print("write frame into video fail", err)
