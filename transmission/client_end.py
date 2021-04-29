import base64
import json
# import mmap
import cv2

from client.local_store import LocalStore
from client.offloading import send_frame
from client.preprocessing import PreProcessing
from tools import make_request
from client.decision_engine import DecisionEngine
from tools.network_condition import get_network_condition
from tools.transfer_files_tool import save_file, transfer_file_to_str, transfer_array_and_str
from client.video_reader import VideoReader


class Client:
    """
    initialize Client end
    """
    def __init__(self, input_file, file_type, service_type):

        self.input_file = input_file
        self.initial_url = "http://127.0.0.1:5000/initial"
        self.picture_url = "http://127.0.0.1:5000/pictures_handler"
        self.video_file_url = "http://127.0.0.1:5000/video_file_handler"
        # initial_url = "http://39.99.145.157:5000/initial"
        # picture_url = "http://39.99.145.157:5000/pictures_handler"
        # video_file_url = "http://39.99.145.157:5000/video_file_handler"
        # initialize local store
        self.local_store = LocalStore()

        # initialize video reader
        self.reader = VideoReader(input_file)

        # get initial network condition
        service_delay, net_speed = get_network_condition(self.initial_url)

        # initialize decision engine
        assert file_type is not None
        assert file_type == 'image' or file_type == 'video'
        self.file_type = file_type
        assert file_type is not None
        assert service_type == 'image classification' or service_type == 'object detection'
        self.service_type = service_type
        requirement_type = (file_type, service_type)
        decision_engine = DecisionEngine(
            service_delay=service_delay, requirement_type=requirement_type, net_condition=net_speed
        )
        self.msg_dict, self.selected_model = decision_engine.get_decision_result()

        # initialize preprocess module
        self.preprocessing = PreProcessing()











