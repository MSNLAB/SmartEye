from PIL import Image
import os


def image_size_adjust(image_size, input_file):
    """
    according to the image_size stored in message responsed by the server,
    client adjusts the image size of image which will be sent to the server

    :param image_size: image size, support 100×100 poxels， 500x500 pixels
    :param input_file: images which needs to be adjust
    :return:
    """

    image = Image.open(input_file)
    if image.size == image_size:
        return
    result = image.resize(image_size, Image.ANTIALIAS)
    result.save(input_file)



def video_bitrate_adjust(input_file, bitrate):
    """
    adjust the input_file's bitrate according to the parameter bitrate

    :param input_file: video file path
    :param bitrate: the bitrate value of video transfered to
    :return:
    """
    result = input_file
    cmd = ("ffmpeg -i " + input_file + " -b:v " + bitrate +
           " -maxrate 2M " + " -bufsize 2M " + result)
    os.system(cmd)


def video_resolution_adjust(input_file, resolution):
    """
    adjust the input_file's resolution according to the parameter resolution
    :param input_file: video file path
    :param resolution: the resolution value of video transfered to
    :return:
    """
    result = input_file
    cmd = "ffmpeg -i " + input_file + " -vf scale=" + resolution + " " + result
    os.system(cmd)


if __name__ == '__main__':

    image_size_adjust((500, 500), './gile1.jpg')