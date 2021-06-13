import common
from tools.read_config import read_config

import random
from loguru import logger


class DecisionEngine:
    """Decision engine

    decide the basic information of image and video:
        the size of single image,
        the bitrate and resolution of video
    by the network condition
    This module should return a max value, for example,
    bitrate=1000k means the biggest birate of video transmitted
    should not over 1000k
    """

    def __init__(self, *requirement_type): # **initial_dict
        """
        :param initial_dict: this is a dict type, including service_delay, requirements and netcondition
        """
        self.requirement_type = requirement_type
        self.object_detection_models = read_config("object-detection")
        self.image_classification_models = read_config("image-classification")

    def get_result(self, local_cpu_usage, local_memory_usage, sys_info):
        """Decide to choose local processor or remote processor

        :param: local_cpu_usage: local cpu's usage
        :param: local_memory_usage: local memory's usage
        :param: sys_info: system information including cpu usage list and memory usage list
        :return: flag: the flag of remote or local processing
                 msg_dict: message dict
                 selected_model: selected model name
        """
        if local_cpu_usage < 50 and local_memory_usage < 50:
            flag = common.LOCAL
        else:
            flag = common.OFFLOAD

        msg_dict, selected_model = self.get_decision(flag, sys_info)
        return flag, msg_dict, selected_model

    def get_decision(self, flag, sys_info):
        """Decide the model and image resolution

        :param flag: the flag of remote or local processing
        :param: sys_info: system information including cpu usage list and memory usage list
        :return: msg_dict: message dict
                 selected_model: selected model name
        """

        if flag == common.OFFLOAD:
            if self.requirement_type[0] == common.IMAGE_TYPE:
                if len(sys_info.processing_delay) == 0:
                    msg_dict = self.decide_image_size(0)
                    selected_model = self.decide_model(0, self.requirement_type[1])
                else:
                    msg_dict = self.decide_image_size(sys_info.processing_delay[-1])
                    selected_model = self.decide_model(sys_info.processing_delay[-1], self.requirement_type[1])

            elif self.requirement_type[0] == common.VIDEO_TYPE:
                if len(sys_info.processing_delay) == 0:
                    msg_dict = self.decide_bitrate_and_resolution(0)
                    selected_model = self.decide_model(0, self.requirement_type[1])
                else:
                    msg_dict = self.decide_bitrate_and_resolution(sys_info.processing_delay[-1])
                    selected_model = self.decide_model(sys_info.processing_delay[-1], self.requirement_type[1])

            return msg_dict, selected_model
        else:
            if self.requirement_type[0] == common.IMAGE_TYPE:
                msg_dict = {}
                selected_model = self.decide_local_model(self.requirement_type[1])

            elif self.requirement_type[0] == common.VIDEO_TYPE:
                msg_dict = {}
                selected_model = self.decide_local_model(self.requirement_type[1])

            return msg_dict, selected_model

    def decide_qp(self, processing_delay):
        """Decide the image qp

        :param processing_delay: processing delay
        :return: qp number
        """
        qp_list = [i for i in range(0, 52)]
        # select the first for test
        qp = qp_list[0]
        return qp

    def decide_image_size(self, processing_delay):
        """Decide the image size according to the content of initial_dict

        :param processing_delay: processing delay
        :return: image size dict
        """
        image_size_dict = {}

        image_size = (500, 500)
        return_dict = {
            'image_size': image_size
        }

        return return_dict

    def decide_bitrate_and_resolution(self, processing_delay):
        """Decide the image size according to the content of initial_dict

        :param processing_delay: processing delay
        :return: bitrate and resolution dict
        """
        return_dict = {'bitrate': '1000k',
                       'resolution': '1920:1080'}

        return return_dict

    def decide_model(self, processing_delay, serv_type):
        """Decide the computation model according to the content of initial_dict

        :param processing_delay: processing delay
        :param serv_type: server type
        :return: selected model
        """
        if serv_type == common.IMAGE_CLASSIFICATION:
            rdn = random.randint(0, len(read_config("image-classification"))-1)
            model = self.image_classification_models[rdn]
        else:
            rdn = random.randint(0, len(read_config("object-detection")) - 1)
            model = self.object_detection_models[rdn]
        return model

    def decide_local_model(self, serv_type):
        """Decide local model

        :param serv_type: server type
        :return: selected model
        """
        rdm = random.randint(0, 1)
        if serv_type == common.IMAGE_CLASSIFICATION:
            model = self.image_classification_models[rdm]
        else:
            model = self.object_detection_models[rdm+2]
        return model


if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

