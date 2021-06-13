import base64
import json
from urllib import request, parse
import time
from loguru import logger


def make_request(url, **msg_dict):
    """Send info to server.

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
    try:
        response = request.urlopen(req)
        t2 = time.time()
        result = response.read().decode('utf-8')
    except:
        logger.exception("Error request server!")
    else:
        result_dict = json.loads(result)
        try:
            processing_delay = t2 - t1
            arrive_transfer_server_time = (processing_delay - result_dict["process_time"]) / 2
            assert processing_delay != 0
            assert arrive_transfer_server_time != 0
        except AssertionError as err:
            logger.error("processing_delay or arrive_transfer_server_time is 0!")
        else:
            logger.debug("make request well!")
            return result_dict, t1, processing_delay, arrive_transfer_server_time


if __name__ == "__main__":
    url = "1"
    service_delay = 0
    service_type = 0
    net_condition = 0
    make_request(url, service_delay, service_type, net_condition)