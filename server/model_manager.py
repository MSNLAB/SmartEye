import json
import os
import sys

import psutil
import torch
import global_variable
from server.grpc_config import msg_transfer_pb2
from tools.read_config import read_config
from torchvision.models.detection import *
from torchvision.models import *


def load_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """
    loaded_models = global_variable.loaded_model_dict.keys()

    if selected_model in loaded_models:
        model = eval(selected_model)()
        model.load_state_dict(global_variable.loaded_model_dict[selected_model], False)
    else:
        # weight_folder = read_config("models-path", "path")
        weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
        try:
            for file in os.listdir(weight_folder):
                if selected_model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            print("there is no matched file!")
        # print(selected_model)
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        global_variable.loaded_model_dict[selected_model] = file_load
        model = eval(selected_model)()
        model.load_state_dict(file_load, False)
    model.eval()
    return model


def uninstall_model(model_name):

    del global_variable.loaded_model_dict[model_name]


def get_server_cpu_usage():

    cpu_usage = psutil.cpu_percent()
    cpu_usage_reply = msg_transfer_pb2.Cpu_Usage_Reply(cpu_usage=cpu_usage)
    return cpu_usage_reply
