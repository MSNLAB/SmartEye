import base64
import json
# import mmap
import cv2
import os
from local.local_store import LocalStore
from local.offloading import send_frame
from local.preprocessing import PreProcessing
from tools import make_request
from local.decision_engine import DecisionEngine
from tools.network_condition import get_network_condition
from tools.transfer_files_tool import transfer_file_to_str, transfer_array_and_str
from local.video_reader import VideoReader
from tools.read_config import read_config
from local.system_infomation import SysInfo
import local.local_processing


class Client:
    """
    initialize Client end
    """
    def __init__(self, input_file, file_type, service_type, store_type=None):

        self.input_file = input_file
        assert file_type is not None
        assert file_type == 'image' or file_type == 'video'
        self.file_type = file_type
        assert file_type is not None
        assert service_type == 'image classification' or service_type == 'object detection'
        self.service_type = service_type
        # initialize local store
        self.local_store = LocalStore(store_type)

        # initialize video reader
        self.reader = VideoReader(input_file)

        # initialize decision engine
        requirement_type = (file_type, service_type)
        self.decision_engine = DecisionEngine(requirement_type=requirement_type)
        # self.msg_dict, self.selected_model = decision_engine.get_decision_result(service_delay, net_speed)

        # initialize preprocess module
        self.preprocessing = PreProcessing()

        self.initial_url = read_config("transfer-url", "initial_url")
        self.picture_url = read_config("transfer-url", "picture_url")
        self.video_file_url = read_config("transfer-url", "video_file_url")
        # # initial_url = "http://39.99.145.157:5000/initial"
        # # picture_url = "http://39.99.145.157:5000/pictures_handler"
        # # video_file_url = "http://39.99.145.157:5000/video_file_handler"
        # get initial network condition
        service_delay, net_speed = get_network_condition(self.initial_url)
        self.info = SysInfo(os.path.basename(input_file).split(".")[0])
        self.info.append(service_delay, net_speed)








