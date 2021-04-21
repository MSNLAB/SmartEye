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
    def __init__(self, input_source):

        self.input_source = input_source
        assert input_source is not None
        self.cap = cv2.VideoCapture(self.input_source)

    def read_camera(self):
        """
        camera interface: read image frames from camera(virtual camera)
        :param: device: device number
        :return: video frame in type class 'numpy.ndarray'
        """

        assert type(self.input_source) == 'int'

        if self.cap.isOpened():

            ret, frame = self.cap.read()
            return frame
        else:
            self.cap.release()
            return None

    def read_file(self):
        """
        file interface: read image frames from video file
        :param: input_file: file path which will be read
        :return: video frame in type class 'numpy.ndarray'
        """
        # print(type(self.input_source) is 'str')
        assert isinstance(self.input_source, str)
        if self.cap.isOpened():

            ret, frame = self.cap.read()
            return frame
        else:
            self.cap.realease()
            return None




if __name__ == "__main__":

    video = '/home/wxz/Desktop/20200827153531.mp4'
    reader = VideoReader()
    frame = reader.read_file(video)
    print(type(frame))
