import common
# from local.local_info import get_local_utilization
from tools.read_config import read_config
from local import globals


class DecisionEngine:
    """
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
        """
        decide to choose local processor or remote processor
        :return: 'local' for local processor and 'remote' for remote processor
        """
        if local_cpu_usage < 0 and local_memory_usage < 100:
            flag = common.LOCAL
            # return common.LOCAL
        else:
            flag = common.OFFLOAD
            # return common.OFFLOAD
        msg_dict, selected_model = self.get_decision(flag, sys_info)
        return flag, msg_dict, selected_model

    def get_decision(self, flag, sys_info):   # sys_info=None

        if flag == common.OFFLOAD:
            if self.requirement_type[0] == common.IMAGE_TYPE:
                if len(sys_info.processing_delay) == 0:
                    msg_dict = self.decide_image_size(0)
                    selected_model = self.decide_model(0, self.requirement_type[1])
                else:
                    print("mark")
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

        qp_list = [i for i in range(0, 52)]
        # select the first for test
        qp = qp_list[0]
        return qp

    def decide_image_size(self, processing_delay):
        """
        decide the image size according to the content of initial_dict
        :return: image size dict
        """

        image_size_dict = {}

        image_size = (500, 500)
        return_dict = {
            'image_size': image_size
        }

        return return_dict

    def decide_bitrate_and_resolution(self, processing_delay):
        """
        decide the image size according to the content of initial_dict
        :return: bitrate and resolution dict
        """
        return_dict = {'bitrate': '1000k',
                       'resolution': '1920:1080'}

        return return_dict

    def decide_model(self, processing_delay, serv_type):
        """
        decide the computation model according to the content of initial_dict
        :return: selected model
        """
        if serv_type == common.IMAGE_CLASSIFICATION:
            model = self.image_classification_models[0]
        else:
            model = self.object_detection_models[1]
        return model

    def decide_local_model(self, serv_type):

        if serv_type == common.IMAGE_CLASSIFICATION:
            model = self.image_classification_models[0]
        else:
            model = self.object_detection_models[1]
        return model


if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

