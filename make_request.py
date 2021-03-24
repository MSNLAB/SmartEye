from urllib import request, parse
import time


def make_request(url, initial=False, **msg_dict):
    """

    :param url:
    :param dict:
    :return:
    """
    # print(msg_dict)
    headers = {
        # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        # 'Host': 'httpbin.org'
    }
    data = bytes(parse.urlencode(msg_dict), encoding='utf8')
    t1 = time.time()
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    if initial:
        t2 = time.time()
        return response, (t2 - t1)
    else:
        return response




if __name__ == "__main__":
    url = "1"
    service_delay = 0
    service_type = 0
    net_condition = 0
    make_request(url, service_delay, service_type, net_condition)