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
import os
camera_image_save_path = "/home/wxz/Videos/"


class Reader:
    """
    Read image frames from camera or video files
    """

    def __init__(self, video=None):
        self.camera_image_save_path = camera_image_save_path
        self.video = video
        if self.video is None:
            self.video = 1
        self.cap = cv2.VideoCapture(self.video)

    def read_from_camera(self):
        """
        read image frames from camera(virtual camera)
        :return:
        """
        image = "image_%05d.jpg"
        camera_image_name = os.path.join(self.camera_image_save_path, image)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if frame is None:
                break
            cv2.imwrite(camera_image_name, frame)

    def read_from_file(self):
        """
        read image frames from a video file.
        """
        video_name = os.path.split(self.video)[1]
        image_path_pre = os.path.split(self.video)[0]
        video_name_pre = video_name.split(".")[0]
        image_path = os.path.join(image_path_pre, video_name_pre)
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        image_name = video_name_pre + "_%05d.jpg"
        image_store_path = os.path.join(image_path, image_name)
        # print(image_store_path)
        # image_store_path = "image_%05d.jpg"
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if frame is None:
                break
            cv2.imwrite(image_store_path, frame)

    def save_video_file(self):
        """
        read camera and save as video file
        """
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'),
                              15.0, (640, 480))
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 0)
                out.write(frame)
            # self.cap.release()
        out.release()


if __name__ == "__main__":

    video = '/home/wxz/Desktop/20200827153531.mp4'
    reader = Reader()
    reader.save_video_file()
