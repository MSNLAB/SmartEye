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
import cv2


class VideoReader:
    """
    Read image frames from camera or video files
    """

    def read_camera(self, device):
        """
        camera interface: read image frames from camera(virtual camera)
        :param: device: device number
        :return: video frame in type class 'numpy.ndarray'
        """
        assert device is not None
        assert type(device) == 'int'

        cap = cv2.VideoCapture(device)

        if cap.isOpened():

            ret, frame = cap.read()

            if frame is None:
                return None

            return frame

    def read_file(self, input_file):
        """
        file interface: read image frames from video file
        :param: input_file: file path which will be read
        :return: video frame in type class 'numpy.ndarray'
        """
        assert input_file is not None

        cap = cv2.VideoCapture(input_file)

        if cap.isOpened():

            ret, frame = cap.read()

            if frame is None:
                return None

            return frame


if __name__ == "__main__":

    video = '/home/wxz/Desktop/20200827153531.mp4'
    reader = VideoReader()
    frame = reader.read_file(video)
    print(type(frame))
