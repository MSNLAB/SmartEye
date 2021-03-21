
# 怎么根据服务延迟和网络状况做出相应的决定

class dedecision_engine:
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
        self.requirements = initial_dict['requirements']
        self.netcondition = initial_dict['netcondition']
        self.model_list = []
        if self.requirements == "image":
            return self.decide_image_size()
        elif self.requirements == 'video':
            return self.decide_bitrate_and_resolution()


    def decide_image_size(self):
        """
        decide the image size and computation model according to the content of initial_dict
        :return: image size and computation model
        """
        #关于决定图像尺寸和计算模型的条件还需要考虑和调研，比如 网速在什么范围内适合传输（500，500）尺寸的图像，使用复杂度为多少的计算模型
        #要不要写成一个类， 什么时候该写成类，还是得学习
        image_size_dict = {}

        image_size = (500, 500)
        model = 1

        return image_size, model

    def decide_bitrate_and_resolution(self):
        """
        decide the image size and computation model according to the content of initial_dict
        :return:
        """
        bitrate_dict = {}
        resolution_dict = {}

        return bitrate_dict, resolution_dict, self.model_list





if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    # decision_engine(**initial_dict)

