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
from tools.read_config import read_config


class LocalStore:
    """
    according to the requirements, LocalStore stores the input video frame
    as image or video in local directory
    """

    def __init__(self, store_type):
        time = datetime.datetime.now()
        store_path = read_config("store-folder", "store_path")
        self.result_store_location = os.path.join(
            store_path, time.strftime('%a%b%d%H%M')
        )
        if store_type == "video":
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
        # if there is a error breaking the program, all executions before should rollback
        if not os.path.exists(self.result_store_location):
            os.mkdir(self.result_store_location)
        try:
            cv2.imwrite(os.path.join(self.result_store_location, "out_%5d.png"), frame)
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


if __name__ == "__main__":
    local_store = LocalStore()

