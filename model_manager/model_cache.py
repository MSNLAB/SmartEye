import os
import torch
from tools.read_config import read_config
from loguru import logger


def load_model():
    """Load the specified models, return: loaded models"""
    loaded_model = {}
    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    preload_models = read_config("edge-model")

    for model in preload_models:
        try:
            for file in os.listdir(weight_folder):
                if model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            logger.exception("no matched weight file")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        loaded_model[model] = file_load
    return loaded_model

