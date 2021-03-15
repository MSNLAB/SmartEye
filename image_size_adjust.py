from PIL import Image


def image_size_adjust(image_size, input_file):
    """

    according to the image_size stored in message responsed by the server,
    client adjusts the image size of image which will be sent to the server

    :param image_size: image size, support 100×100 poxels， 500x500 pixels
    :param input_file: images which needs to be adjust
    :return:
    """
    print(image_size)
    image = Image.open(input_file)
    if image.size == image_size:
        return
    print(image.size)
    result = image.resize(image_size, Image.ANTIALIAS)
    result.save('gile1.jpg')
    # print(result.size)



if __name__ == '__main__':

    image_size_adjust((500, 500), './gile1.jpg')