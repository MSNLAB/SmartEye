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
import os
import cv2
import datetime
import common
# from tools.read_config import read_config


class LocalStore:
    """
    according to the requirements, LocalStore stores the input video frame
    as image or video in local directory
    """

    def __init__(self, store_type=None):
        time = datetime.datetime.now()
        store_path = os.path.join(os.path.dirname(__file__), "../info_store/handled_result")
        self.n = 0
        self.result_store_location = os.path.join(
            store_path, time.strftime('%a%b%d%H%M')
        )
        if store_type == common.VIDEO_TYPE:
            video_name = time.strftime('%a%b%d%H%M') + ".mp4"
            self.out = cv2.VideoWriter(
                video_name, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480)
            )

    def store_image(self, frame):
        """
        store frame as image
        :param frame: image which will be stored, type numpy.narray
        :return:
        """
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            image_path = os.path.join(self.result_store_location, "out"+self.n+".png")
            cv2.imwrite(image_path, frame)
            self.n += 1
        except Exception as err:
            print("save image fail:", err)

    def store_video(self, frame):
        """
        write a image frame into a video file.
        :param frame: image which will be written, type numpy.ndarray
        :return: None
        """
        try:
            self.out.write(frame)
        except Exception as err:
            print("write frame into video fail", err)


if __name__ == "__main__":
    local_store = LocalStore()


