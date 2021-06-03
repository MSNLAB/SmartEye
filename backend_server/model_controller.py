import os
import psutil
import torch
import globals
from backend_server.grpc_config import msg_transfer_pb2
from tools.read_config import read_config
from torchvision.models.detection import *
from torchvision.models import *


def load_model_files_advance():
    """
    load model files in advance into memory
    :return:
    """
    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    preload_models = read_config("preload-models")

    for model in preload_models:
        try:
            for file in os.listdir(weight_folder):
                if model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            print("there is no matched file!")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        globals.loaded_model[model] = file_load


def load_a_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """
    loaded_models = globals.loaded_model.keys()

    if selected_model in loaded_models:
        model = eval(selected_model)()
        model.load_state_dict(globals.loaded_model[selected_model], False)
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
        globals.loaded_model[selected_model] = file_load
        model = eval(selected_model)()
        model.load_state_dict(file_load, False)
    model.eval()
    return model


def unload_model(model_name):

    del globals.loaded_model[model_name]


def get_server_cpu_usage():

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    cpu_usage_reply = msg_transfer_pb2.Cpu_Usage_Reply(cpu_usage=cpu_usage, memory_usage=memory_usage)
    return cpu_usage_reply
