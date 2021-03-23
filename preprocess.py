from PIL import Image
import os
import subprocess


def image_size_adjust(input_file, image_size):
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
    path = ''
    return path


def video_resolution_and_bitrate_adjust(input_file, **b_r_dict):
    """
    adjust the input_file's resolution and bitrate according to the parameter b_r_tuple
    :param input_file: video file path
    :param b_r_tuple: the max b_r_tuple value of video transfered to
    :return:
    """
    result = input_file
    cmd = ("ffmpeg -i " + input_file + " -vf scale=" + b_r_dict['resolution'] +
        " -b:v " + b_r_dict['bitrate'] + " -maxrate " + b_r_dict['bitrate'] +
        " -bufsize 2M " + result)
    # os.system(cmd)
    # try:
    # except:
    p = subprocess.Popen(cmd)
    p.returncode



# def video_bitrate_adjust(input_file, bitrate):
#     """
#     adjust the input_file's bitrate according to the parameter bitrate
#
#     :param input_file: video file path
#     :param bitrate: the bitrate value of video transfered to
#     :return:
#     """
#
#     # function should get the original bitrate of input_file
#     # and then transfer to the target bitrate
#     # of course, the bitrate value should belong to a bitrate list
#
#
#     result = input_file
#     cmd = ("ffmpeg -i " + input_file + " -b:v " + bitrate +
#            " -maxrate 2M " + " -bufsize 2M " + result)
#     os.system(cmd)


# def get_info(input_file, get_info):
#
#     json_file_name = os.path.basename(input_file).split(".")[0]
#     video_info_cmd = ("ffprobe -i " + input_file + " -v quiet -print_format json -show_streams -select_streams v:0 > "
#                       + json_file_name + ".json")
#     os.system(video_info_cmd)
#
#     with open(json_file_name + ".json", 'r') as f:
#         info = json.load(f)
#         origin_bitrate = info["streams"][0]["bit_rate"]
#         origin_resolution = str(info["streams"][0]["width"]) + ":" + str(info["streams"][0]["height"])
#
#     if get_info == "bitrate":
#         return origin_bitrate
#     else:
#         return origin_resolution


if __name__ == '__main__':

    image_size_adjust((500, 500), './gile1.jpg')