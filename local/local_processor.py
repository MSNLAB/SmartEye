import os
from loguru import logger
import torch
from torchvision.models import *
from model_manager import object_detection, image_classification
from tools.read_config import read_config
from torchvision.models.detection import *

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
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        # logger.debug(model)
        if selected_model in object_detection_models:
            frame_handled = object_detection.object_detection_api(frame, model, threshold=0.8)
            return frame_handled
        elif selected_model in image_classification_models:
            result = image_classification.image_classification(frame, model)
            return result
