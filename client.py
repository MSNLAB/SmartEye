from urllib import request, parse
import base64
import time
import extractframes
import os
import preprocess
# import mmap
import subprocess
import make_request
from decision_engine import DecisionEngine
from transfer_files_tool import save_file, transfer_file_to_str


initial_url = "http://39.99.145.157:5000/initial"
picture_url = "http://39.99.145.157:5000/pictures_handler"
video_file_url = "http://39.99.145.157:5000/video_file_handler"

# url = 'http://39.99.145.157:5000/hello'


class Client:
    """
    Serve as the AR client
    """

    def __init__(self, service_type):
        """
        :param service_type: the kind of input file: image, video
        """
        # self.input_file = input_file
        self.initial_url = initial_url
        self.picture_url = picture_url
        self.video_file_url = video_file_url

        self.service_delay = 0
        self.service_type = service_type
        self.net_condition = self.initial_network_condition()

        self.msg_dict, selected_model = DecisionEngine(service_delay=self.service_delay,
                                                       service_type=self.service_type, net_condition=self.net_condition)

        # send initial condition to the server
        response = make_request.make_request(self.initial_url, selected_model=selected_model)

        # if self.service_type == "image":
        #     self.image_size = response.read().decode('utf-8')
        # else:
        #     self.b_r_tuple = response.read().decode('utf-8')
        # print('mark2')
        # print(self.image_size)

    # picture interface
    def process_picture(self, input_file):

        path = preprocess.image_size_adjust(image_size=self.image_size, input_file=input_file)
        img_str = transfer_file_to_str(path)
        response = make_request.make_request(self.picture_url, img_data=img_str)

        img = response.read().decode('utf-8')
        save_file(img)

    # video file interface
    def process_video_file(self, input_file):

        preprocess.video_resolution_and_bitrate_adjust(input_file, self.msg_dict)
        with open(input_file, 'rb') as f:
            video_byte = base64.b64encode(f.read())
            video_str = video_byte.decode('ascii')
        response = make_request.make_request(self.video_file_url, video_str)
        re = response.read().decode('utf-8')

    def initial_network_condition(self):

        cmd = "ping 39.99.145.157 -n 4"
        s = subprocess.getoutput(cmd)
        # print('a')
        last_line = s.split("\n")[-1]
        avg = last_line.split("=")[-1][:-2]
        return avg
        # print(avg)
        # print(s)
        # with open('initial_condition.txt', 'r') as f:
        #     avg_time = f.read()
        # print(avg_time)

        # print('%s' % (t2 - t1))
        # print('#' * 50)


if __name__ == '__main__':

    input_file = "./98368268-1-208.mp4"
    client = Client('video')
    t1 = time.time()
    # client.process_video_file(input_file)
    t2 = time.time()
    # print(t2 - t1)
