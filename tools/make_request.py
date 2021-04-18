import base64
import json
from urllib import request, parse
import time

import numpy


def make_request(url, **msg_dict):
    """

    :param url: server url
    :param frame: data passing to server
    :param selected_model:
    :return: response object and service delay
    """
    # if "frame" in msg_dict.keys():
    #     print(type(msg_dict["frame"]))
    headers = {
        "User-Agent": "Mozilla",
        # 'content-type': 'application/json'
    }
    # if type(file) is numpy.ndarray:
    #     img_byte = base64.b64encode(file.tostring())
    #     file = img_byte.decode('ascii')
    # msg_dict["file"] = file
    data = parse.urlencode(msg_dict).encode('utf8')
    # print(type(data))
    t1 = time.time()
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    # print(req.data)
    response = request.urlopen(req)
    t2 = time.time()
    return response, (t2 - t1) / 2


if __name__ == "__main__":
    url = "1"
    service_delay = 0
    service_type = 0
    net_condition = 0
    make_request(url, service_delay, service_type, net_condition)