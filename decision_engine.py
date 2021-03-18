


def decision_engine(**initial_dict):
    """
    decide the image size and computation model according to the content of initial_dict
    :param initial_dict: this is a dict type, including service_delay, requirements and netcondition
    :return: image size and computation model
    """
    #关于决定图像尺寸和计算模型的条件还需要考虑和调研，比如 网速在什么范围内适合传输（500，500）尺寸的图像，使用复杂度为多少的计算模型
    #要不要写成一个类， 什么时候该写成类，还是得学习
    image_size_dict = {}
    model_lsit = []
    image_size = (500, 500)
    model = 1

    return image_size, model

if __name__ == '__main__':

    initial_dict = {'service_delay':0, 'requirements':0, 'netcondition':0}
    decision_engine(**initial_dict)

