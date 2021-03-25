import json
from urllib import request, parse
import base64
import time
import video_handle_tool
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
test_package_path = "./test.zip"

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

        self.service_delay = self.initial_network_condition()
        self.service_type = service_type
        # kb/s
        self.net_condition = os.path.getsize(test_package_path) / (float(1024) * self.service_delay)
        # print(self.service_delay)
        decision_engine = DecisionEngine(service_delay=self.service_delay,
                                         service_type=self.service_type, net_condition=self.net_condition)
        if self.service_type == "image":

            self.msg_dict = decision_engine.decide_image_size()
            # print(self.msg_dict['image_size'])

            selected_model = decision_engine.decide_model()

        elif self.service_type == 'video':
            self.msg_dict = decision_engine.decide_bitrate_and_resolution()
            selected_model = decision_engine.decide_model()

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

        # print(self.msg_dict)
        picture_path = preprocess.image_size_adjust(input_file, image_size=self.msg_dict['image_size'])
        msg_dict = transfer_file_to_str(picture_path)
        # print(msg_dict['file_str'])
        #
        # print(type(msg_dict.keys()))
        response = make_request.make_request(self.picture_url, **msg_dict)  # unpack
        msg_str = response[0].read().decode('utf-8')
        msg_dict = json.loads(msg_str)

        save_file(picture_path, **msg_dict)

    # video file interface
    def process_video_file(self, input_file):

        try:
            file_path = preprocess.video_resolution_and_bitrate_adjust(input_file, **self.msg_dict)
        except:
            pass
        else:
            msg_dict = transfer_file_to_str(file_path)
            response = make_request.make_request(self.video_file_url, **msg_dict)
            video = response.read().decode('utf-8')
            save_file(video, input_file)

    def initial_network_condition(self):

        test_str = transfer_file_to_str(test_package_path)
        response, service_delay = make_request.make_request(self.initial_url, img_data=test_str)
        print(response)
        result = response.read().decode('utf-8')
        if result == 'ok':
            print('ok')

        # cmd = "ping 39.99.145.157 -n 4"
        # s = subprocess.getoutput(cmd)
        # # print('a')
        # last_line = s.split("\n")[-1]
        # avg = last_line.split("=")[-1][:-2]
        # return avg
        return service_delay


if __name__ == '__main__':

    input_file = "./85652500-1-192.mp4"
    client = Client('video')
    t1 = time.time()
    client.process_video_file(input_file)
    t2 = time.time()
    # print(t2 - t1)
