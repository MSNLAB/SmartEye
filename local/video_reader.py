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
import common
from tools.read_config import read_config


class VideoReader:
    """Video Reader.

    Read image frames from camera or video files:
        input file path for reading video file;
        input camera device number for reading camera;
    """
    def __init__(self, input_source, camera_type):
        if input_source is not None:
            self.input_source = input_source
            self.cap = cv2.VideoCapture(input_source)
        elif camera_type is not None:

            if camera_type == common.VIRTUAL_CAMERA:
                self.input_source = 1
                self.cap = cv2.VideoCapture(input_source)
            elif camera_type == common.REAL_CAMERA:
                account = read_config("camera-info", "account")
                password = read_config("camera-info", "password")
                ip_address = read_config("camera-info", "ip_address")
                channel = int(read_config("camera-info", "channel"))
                video_stream_path = "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (
                    account, password, ip_address, channel)

                self.cap = cv2.VideoCapture(video_stream_path)

    def read_frame(self):
        """Read frame of video.

        :return: video frame in type class 'numpy.ndarray'
        """
        if self.cap.isOpened():

            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                self.cap.release()
                return None


if __name__ == "__main__":

    video = 'D:\PyCharm 2020.3.1\workspace\\video2edge\85652500-1-192.mp4'
    reader = VideoReader(video, 9)
    frame = reader.read_frame()
    # print(type(frame))
