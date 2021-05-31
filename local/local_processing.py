#!/usr/bin/env python
# encoding: utf-8
'''
@author: XuezhiWang
@license:
@contact: 1050642597@qq.com
@software: pycharm
@file: local_processing.py
@time: 2021/4/16 下午2:33
@desc:
'''
import os

from model_manager import object_detection, image_classification
from tools.read_config import read_config

object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


def load_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """
    # weight_folder = read_config("models-path", "path")
    weight_folder = os.path.join(os.path.dirname(__file__), "../modelweightfile")
    try:
        for file in os.listdir(weight_folder):
            print(file)
            if selected_model in file:
                file_name = file
                break
        assert file_name is not None
    except AssertionError:
        print("there is no matched file!")
    # weight_files_path = os.path.join(weight_folder, file_name)
    # model = eval(selected_model)()
    # model.load_state_dict(torch.load(weight_files_path), False)
    # model.eval()
    # return model


class LocalProcessing:
    """
    providing some local simple processing functions, such as simple neural network
    """
    def __init__(self, input_file, service_type, store_type):

        self.input_file = input_file
        self.service_type = service_type

    def process(self, frame, selected_model):
        model = load_model(selected_model)
        if selected_model in object_detection_models:
            frame_handled = object_detection.object_detection_api(frame, model, threshold=0.8)
            # store

        else:
            result = image_classification.image_classification(frame, selected_model)


if __name__ == "__main__":
    # load_model("s")
    pass
