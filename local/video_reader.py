import cv2
from tools.read_config import read_config


class VideoReader:
    def __init__(self, input_source=None, rtsp_camera=None):
        self.input_source = None
        if input_source:
            self.input_source = input_source
        elif rtsp_camera:
            account = read_config("camera-info", "account")
            password = read_config("camera-info", "password")
            ip_address = read_config("camera-info", "ip_address")
            channel = int(read_config("camera-info", "channel"))
            self.input_source = "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" \
                                % (account, password, ip_address, channel)
        self.cap = cv2.VideoCapture(self.input_source)

     """read a video frame from the camera or video file, return type: numpy.ndarray"""
    def read_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
            self.cap.release()
            return None
        return None
