from urllib import request, parse
import time


def make_request(url, frame):
    """

    :param url: server url
    :param frame: data passing to server
    :return: response object and service delay
    """
    headers = {
        # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        # 'Host': 'httpbin.org'
    }
    data = bytes(parse.urlencode(frame), encoding='utf8')
    t1 = time.time()
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    t2 = time.time()
    return response, (t2 - t1) / 2


if __name__ == "__main__":
    url = "1"
    service_delay = 0
    service_type = 0
    net_condition = 0
    make_request(url, service_delay, service_type, net_condition)