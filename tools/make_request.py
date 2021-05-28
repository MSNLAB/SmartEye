import base64
import json
from urllib import request, parse
import time

import numpy


def make_request(url, **msg_dict):
    """

    :param url: server url
    :param msg_dict:
    :return: response object and service delay
    """
    headers = {
        "User-Agent": "Mozilla",
        # 'content-type': 'application/json'
    }
    data = parse.urlencode(msg_dict).encode('utf8')
    t1 = time.time()
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    t2 = time.time()
    result = response.read().decode('utf-8')
    result_dict = json.loads(result)
    return result_dict, (t2 - t1) / 2, result_dict["arrive_time"] - t1


if __name__ == "__main__":
    url = "1"
    service_delay = 0
    service_type = 0
    net_condition = 0
    make_request(url, service_delay, service_type, net_condition)