import random
import edge_globals
from tools.read_config import read_config
from loguru import logger


class DecisionEngine:
    def __init__(self, sys_info):
        self.object_detection_models = read_config("object-detection")
        self.image_classification_models = read_config("image-classification")
        self.resolution_list = []
        self.qp_value = 0
        self.sys_info = sys_info
        self.policy_set = {"always_local_fastest_model": self.always_local_fastest_model,
                           "always_cloud_lowest_delay":  self.always_cloud_lowest_delay}


    # the video frame will be always processed on edge
    def always_local_fastest_model(self):
        pro_location = edge_globals.LOCAL
        pre_proc = None
        selected_model = None
        return pro_location, pre_proc, selected_model

    # the video frame will be always processed on the cloud
    def always_cloud_lowest_delay(self):
        pro_location = edge_globals.OFFLOAD
        pre_proc = None
        selected_model = None
        return pro_location, pre_proc, selected_model

    def get_decision(self, policy):
        return self.policy_set[policy]()











