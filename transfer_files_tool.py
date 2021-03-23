import base64


def save_file(file_str):
    """
    save files from a file_str
    :param file_dict:
    :return:
    """
    img_decode_ = file_str.encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    # save the information as .jpg file
    origin_file_path = ''
    with open(origin_file_path, 'wb') as f:
        f.write(img_decode)

    return origin_file_path



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


