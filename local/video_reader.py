#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: video_reader.py
@time: 2021/4/12 下午10:26
@desc:
'''
import os
import sys
import cv2


class VideoReader:
    """
    Read image frames from camera or video files: input file path for reading video file;
    input camera device number for reading camera
    """
    def __init__(self, input_source):
        self.input_source = input_source
        if self.input_source is None:
            self.input_source = 1
        self.cap = cv2.VideoCapture(input_source)

    def read_camera(self):
        """
        camera interface: read image frames from camera(virtual camera)
        :param: device: device number
        :return: video frame in type class 'numpy.ndarray'
        """
        assert type(self.input_source) == 'int'
        if self.cap.isOpened():

            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                self.cap.release()
                return None

    def read_frame(self):
        """
        file interface: read image frames from video file
        :param: input_file: file path which will be read
        :return: video frame in type class 'numpy.ndarray'
        """
        assert isinstance(self.input_source, str), "input is not a str type"
        assert os.path.isfile(self.input_source), "can't find this file"
        if self.cap.isOpened():

            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                self.cap.release()
                return None


if __name__ == "__main__":

    video = 'D:\PyCharm 2020.3.1\workspace\\video2edge\85652500-1-192.mp4'
    reader = VideoReader(video)
    frame = reader.read_file()
    # print(type(frame))
    print(sys.getsizeof(frame))
