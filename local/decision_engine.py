from tools.read_config import read_config


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

    def __init__(self, requirement_type): # **initial_dict
        """
        :param initial_dict: this is a dict type, including service_delay, requirements and netcondition
        """
        self.requirement_type = requirement_type
        self.object_detection_models = read_config("object-detection")
        self.image_classification_models = read_config("image-classification")

    def get_decision_result(self, service_delay, net_speed):

        if self.requirement_type[0] == "image":
            msg_dict = self.decide_image_size(net_speed)
            selected_model = self.decide_model(service_delay, self.requirement_type[1])

        elif self.requirement_type[0] == 'video':
            msg_dict = self.decide_bitrate_and_resolution()
            selected_model = self.decide_model(self.requirement_type[1], self.requirement_type[1])
        return msg_dict, selected_model

    def decide_qp(self):
        pass
    
    def decide_image_size(self, net_speed):
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

    def decide_bitrate_and_resolution(self):
        """
        decide the image size according to the content of initial_dict
        :return: bitrate and resolution dict
        """
        return_dict = {'bitrate': '1000k',
                       'resolution': '1920:1080'}

        return return_dict

    def decide_model(self, total_service_delay, service_type):
        """
        decide the computation model according to the content of initial_dict
        :return: selected model
        """
        if service_type == 'image classification':
            model = self.image_classification_models[0]
        else:
            model = self.object_detection_models[4]
        return model


if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

