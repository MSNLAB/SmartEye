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
        self.requirement_type = initial_dict['requirement_type']
        self.net_condition = initial_dict['net_condition']
        self.object_detection_models = [
            'fasterrcnn_mobilenet_v3_large_320_fpn',
            'fasterrcnn_mobilenet_v3_large_fpn',
            'fasterrcnn_resnet50_fpn',
            'maskrcnn_resnet50_fpn',
            'retinanet_resnet50_fpn'
            ]
        self.image_classification_models = [
            'alexnet',
            'densenet',
            'densenet121',
            'densenet161',
            'densenet169',
            'densenet201',
            'detection',
            'googlenet',
            'inception',
            'inception_v3'
        ]
        #'alexnet', 'densenet', 'densenet121', 'densenet161', 'densenet169', 'densenet201', 'detection', 'googlenet', 'inception', 'inception_v3', 'mnasnet', 'mnasnet0_5', 'mnasnet0_75', 'mnasnet1_0', 'mnasnet1_3', 'mobilenet', 'mobilenet_v2', 'mobilenet_v3_large', 'mobilenet_v3_small', 'mobilenetv2', 'mobilenetv3', 'quantization', 'resnet', 'resnet101', 'resnet152', 'resnet18', 'resnet34', 'resnet50', 'resnext101_32x8d', 'resnext50_32x4d', 'segmentation', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0', 'shufflenet_v2_x1_5', 'shufflenet_v2_x2_0', 'shufflenetv2', 'squeezenet', 'squeezenet1_0', 'squeezenet1_1', 'utils', 'vgg', 'vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn', 'video', 'wide_resnet101_2', 'wide_resnet50_2'

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

    def decide_model(self, service_type):
        """
        decide the computation model according to the content of initial_dict
        :return: selected model
        """
        if service_type == 'image classification':
            model = self.image_classification_models[0]
        else:
            model = self.object_detection_models[0]
        return model


if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

