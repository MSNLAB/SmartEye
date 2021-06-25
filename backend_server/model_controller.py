import os
import psutil
import torch
import backend_globals
from backend_server.grpc_config import msg_transfer_pb2
from tools.read_config import read_config
from torchvision.models.detection import *
from torchvision.models import *
from loguru import logger


def load_model_files_advance():
    """load model files into memory when the server is loaded.

    When the server is loaded, this function gets the preload model names from configure file,
    and loads these models one by one.

    :return: None
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
            logger.exception("there is no matched file!")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        backend_globals.loaded_model[model] = file_load


def load_a_model(selected_model):
    """Load the weight file of selected model.

    There are two cases:
        1. the model has been loaded in advance(when server is loaded)
        2. the model doesn't be loaded
    for the first case, just returns the model directly;
    for the second case, finds the weight file of model, load and return .

    :param selected_model: The name of the model to load
    :return: model: loaded model
    """
    loaded_models = backend_globals.loaded_model.keys()

    if selected_model in loaded_models:
        model = eval(selected_model)()
        model.load_state_dict(backend_globals.loaded_model[selected_model], False)
    else:
        weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
        try:
            for file in os.listdir(weight_folder):
                if selected_model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError as err:
            logger.exception("there is no matched file!")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        backend_globals.loaded_model[selected_model] = file_load
        model = eval(selected_model)()
        model.load_state_dict(file_load, False)
    model.eval()
    return model


def unload_model(model_name):
    """unload the model which is specified by model_name.

    :param model_name: The name of the model to unload
    :return: None
    """
    del backend_globals.loaded_model[model_name]


def get_server_utilization():
    """Get the cpu usage and memory usage of the device.

    Getting the cpu usage and memory usage of the device,
    and then sealing these two data in Server_Utilization_Reply.

    :return: server_utilization_reply, a data structure defined in grpc
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    server_utilization_reply = msg_transfer_pb2.Server_Utilization_Reply(cpu_usage=cpu_usage, memory_usage=memory_usage)
    return server_utilization_reply
