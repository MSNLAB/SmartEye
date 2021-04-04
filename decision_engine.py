import preprocess


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

    def __init__(self, **initial_dict):
        """
        :param initial_dict: this is a dict type, including service_delay, requirements and netcondition
        """
        self.service_delay = initial_dict['service_delay']
        self.service_type = initial_dict['service_type']
        self.net_condition = initial_dict['net_condition']
        self.model_list = ['fasterrcnn_mobilenet_v3_large_320_fpn', 'fasterrcnn_mobilenet_v3_large_fpn',
                           'fasterrcnn_resnet50_fpn', 'maskrcnn_resnet50_fpn', 'retinanet_resnet50_fpn']

        # if self.service_type == "image":
        #     image_size = self.decide_image_size()
        #     selected_model = self.decide_model()
        #     return image_size, selected_model
        # elif self.service_type == 'video':
        #     msg_dict = self.decide_bitrate_and_resolution()
        #     selected_model = self.decide_model()
        #     return msg_dict, selected_model

    def decide_image_size(self):
        """
        decide the image size according to the content of initial_dict
        :return: image size dict
        """
        # 关于决定图像尺寸和计算模型的条件还需要考虑和调研，比如 网速在什么范围内适合传输（500，500）尺寸的图像，使用复杂度为多少的计算模型
        # 要不要写成一个类， 什么时候该写成类，还是得学习
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

    def decide_model(self):
        """
        decide the computation model according to the content of initial_dict
        :return: selected model
        """
        model = 1
        return model


if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

