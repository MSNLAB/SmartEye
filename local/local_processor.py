#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: local_processor.py
@time: 2021/4/16 下午2:33
@desc:
'''
import os

import torch
from torchvision.models import *
import common
# from backend_server.model_controller import load_a_model
from model_manager import object_detection, image_classification
from tools.read_config import read_config
from torchvision.models.detection import *


object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


class LocalProcessor:
    """
    providing some local simple processing functions, such as simple neural network
    """
    def __init__(self, input_file, serv_type, store_type=None):

        self.input_file = input_file
        self.serv_type = serv_type
        self.models = {3: "alexnet",4: "fasterrcnn_mobilenet_v3_large_320_fpn"}
        if serv_type == common.OBJECT_DETECTION:
            self.model = load_model(self.models[4])
        else:
            self.model = load_model(self.models[3])

    def process(self, frame):

        if self.serv_type == common.OBJECT_DETECTION:
            frame_handled = object_detection.object_detection_api(frame, self.model, threshold=0.8)
            return frame_handled
        else:
            result = image_classification.image_classification(frame, self.model)
            return result


def load_model(selected_model):

    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    try:
        for file in os.listdir(weight_folder):
            if selected_model in file:
                file_name = file
                break
        assert file_name is not None
    except AssertionError:
        print("there is no matched file!")
    weight_files_path = os.path.join(weight_folder, file_name)
    file_load = torch.load(weight_files_path)
    model = eval(selected_model)()
    model.load_state_dict(file_load, False)
    model.eval()
    return model


if __name__ == "__main__":
    # load_model("s")
    pass
