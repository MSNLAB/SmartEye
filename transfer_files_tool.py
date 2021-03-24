import base64
import os


def save_file(file_str, picture_path):
    """
    save files from a file_str
    :param file_dict:
    :return:
    """
    origin_file_path = os.path.dirname(picture_path)
    file_pre_name = os.path.basename(picture_path).split('.')[0]
    suffix = os.path.basename(picture_path).split('.')[1]
    file_name = origin_file_path + '\\' + file_pre_name + '_handled.' + suffix
    img_decode_ = file_str.encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    # save the information as .jpg file
    with open(file_name, 'wb') as f:
        f.write(img_decode)

    return file_name


def transfer_file_to_str(file_path):
    """
    transfer image to a string
    :param file_path: file path
    :return: image string
    """
    with open(file_path, 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
        img_str = img_byte.decode('ascii')
    return img_str


