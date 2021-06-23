import os
import sys
import torch
from loguru import logger
from config.model_info import model_lib
from torchvision.models import *
from torchvision.models.detection import *


def load_models(model_list):
    loaded_model = {}
    weight_folder = os.path.join(os.path.dirname(__file__), "../../Downloads/SmartEye/cv_model")
    
    for model_name in model_list:
        if model_name in model_lib.keys():
            weight_files_path = os.path.join(weight_folder, model_lib[model_name]['model_path'])
            # load the weight file
            file_load = torch.load(weight_files_path)
            model = eval(model_name)()
            model.load_state_dict(file_load, False)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            model.eval()
            loaded_model[model_name] = model
        else:
            logger.error('model does not exist')
            sys.exit()
    return loaded_model


def get_fastest_model(model_list):
    fast_model = None
    min_delay = float('inf')
    for model in model_list:
        if model in model_lib.keys():
            delay = model_lib[model]["tx2_delay"]
            if delay < min_delay:
                fast_model = model
                min_delay = delay
    return fast_model
    #return 'retinanet_resnet50_fpn'

def get_most_precise_model(model_list):
    precise_model = None
    max_precision = float('-Inf')
    for model in model_list:
        if model in model_lib.keys():
            precision = model_lib[model]['precision']
            if precision > max_precision:
                precise_model = model
                max_precision = precision
    return precise_model


















