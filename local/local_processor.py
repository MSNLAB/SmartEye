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
from loguru import logger
import torch
from torchvision.models import *
from model_manager import object_detection, image_classification
from tools.read_config import read_config
from torchvision.models.detection import *
import local.globals

object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


class LocalProcessor:
    """Process the image data in the local.

    Provide some local simple processing functions, such as simple neural network
    """
    # def __init__(self, input_file, serv_type, store_type=None):
    #
    #     self.input_file = input_file
    #     self.serv_type = serv_type

    def process(self, frame, selected_model, loaded_model):
        """Process image.

        :param frame: image frame to process
        :param selected_model: selected model name
        """

        model = eval(selected_model)()
        # logger.debug(loaded_model[selected_model])
        model.load_state_dict(loaded_model[selected_model], False)
        model.eval()
        # logger.debug(model)
        if selected_model in object_detection_models:
            frame_handled = object_detection.object_detection_api(frame, model, threshold=0.8)
            return frame_handled
        elif selected_model in image_classification_models:
            result = image_classification.image_classification(frame, model)
            return result


def load_model():
    """Load the specified model

    :param selected_model
    :return: model
    """
    loaded_model = {}
    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    local_preload_models = read_config("local-loaded-models")

    for model in local_preload_models:
        try:
            for file in os.listdir(weight_folder):
                if model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            logger.exception("there is no matched file!")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        loaded_model[model] = file_load
    return loaded_model


if __name__ == "__main__":
    # load_model("s")
    pass
