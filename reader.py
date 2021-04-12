#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: reader.py
@time: 2021/4/12 下午10:26
@desc:
'''
import cv2


class Reader:
    """
    Read image frames from camera or video files
    """

    def __init__(self, video=None):
        self.video = video
        if self.video is None:
            self.video = 1
        self.cap = cv2.VideoCapture(self.video)
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'),
                                   20.0, (640, 480))

    def read_from_camera(self):
        """
        read image frames from camera(virtual camera)
        :return:
        """

        pass

    def read_from_file(self):
        """
        read image frames from a video file.
        """
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 0)
                self.out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        self.out.release()
