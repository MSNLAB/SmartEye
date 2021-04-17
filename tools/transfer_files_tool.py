import base64
import os

server_save_path = './offloading_file/'


def save_file(picture_path=None, **msg_dict):
    """
    :param picture_path: original path of the picture, which has handled by the server
    :param msg_dict: this is a dictionary parameter including file_name and file_str
    :return: save path
    """
    img_decode_ = msg_dict["file_str"].encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    # server end
    if picture_path is not None:
        origin_file_path = os.path.dirname(picture_path)
        file_pre_name = os.path.basename(picture_path).split('.')[0]
        suffix = os.path.basename(picture_path).split('.')[1]
        file_name = origin_file_path + '/' + file_pre_name + '_handled.' + suffix
    # client end
    else:
        if not os.path.isdir(server_save_path):
            os.mkdir(server_save_path)
        file_name = server_save_path + msg_dict['file_name']

    # save the information as .jpg file
    with open(file_name, 'wb') as f:
        f.write(img_decode)

    return file_name


def transfer_file_to_str(file_path):
    """
    transfer image to a string
    :param file_path: file path
    :return: msg_dict including file name and file str encoded by base64 package
    """
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
        img_str = img_byte.decode('ascii')
    msg_dict = {
        'file_name': file_name,
        'file_str': img_str
    }

    return msg_dict

