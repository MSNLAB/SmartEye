import base64
import os
import numpy as np


def transfer_file_to_str(file_path):
    """Transfer image to a string

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


def transfer_array_and_str(frame, way):
    """Transfer between base64 format and numpy.ndarray

    :param frame: will be transfered image str or ndarray
    :param way: if way is 'up', transfer numpy.ndarray format to base64 format,
        else if way is 'down', transfer base64 format format to numpy.ndarray.
    :return: image ndarray or image str
    """
    if way is 'up':
        binary_frame = frame.tobytes()
        img_byte = base64.b64encode(binary_frame)
        img_str = img_byte.decode('ascii')
        return img_str
    else:
        img_decode_ = frame.encode('ascii')
        img_decode = base64.b64decode(img_decode_)
        nprr = np.fromstring(img_decode, np.uint8)
        return nprr


