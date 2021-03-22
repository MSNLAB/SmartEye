from urllib import request, parse
import base64
import time
import extractframes
import os
import preprocess
# import mmap
import subprocess


initial_url = "http://39.99.145.157:5000/initial"
picture_url = "http://39.99.145.157:5000/pictures_handler"
video_file_url = "http://39.99.145.157:5000/video_file_handler"

# url = 'http://39.99.145.157:5000/hello'


class Client:
    """
    Serve as the AR client
    """

    def __init__(self, service_type):
        """
        :param service_type: the kind of input file: image, video
        """
        # self.input_file = input_file
        self.initial_url = initial_url
        self.picture_url = picture_url
        self.video_file_url = video_file_url

        self.service_delay = 0
        self.service_type = service_type
        self.net_condition = self.initial_network_condition()

        # send initial condition to the server
        dict = {
            'service_delay': self.service_delay,
            'requirements': self.service_type,
            'net_condition': self.net_condition
        }
        headers = {
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }

        data = bytes(parse.urlencode(dict), encoding='utf8')
        req = request.Request(url=self.initial_url, data=data, headers=headers, method='POST')

        response = request.urlopen(req)
        if self.service_type == "image":
            self.image_size = response.read().decode('utf-8')
        else:
            self.b_r_tuple = response.read().decode('utf-8')
        # print('mark2')
        # print(self.image_size)

    # picture interface
    def process_picture(self, input_file):

        headers = {
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }

        # read pictures one by one from the picture folder
        folder_path = extractframes.extract_frames(input_file)

        picture_list = os.listdir(folder_path)
        # print(picture_list)
        for picture in picture_list:
            picture_path = folder_path + "\\" + picture
            preprocess.image_size_adjust(image_size=self.image_size, input_file=picture_path)
            with open(picture_path, 'rb') as f:
                img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
                img_str = img_byte.decode('ascii')
            dict = {
                # 'name': 'Germey',
                'image': img_str
            }
            data = bytes(parse.urlencode(dict), encoding='utf8')
            req = request.Request(url=self.picture_url, data=data, headers=headers, method='POST')

            response = request.urlopen(req)
            img = response.read().decode('utf-8')
            img_decode_ = img.encode('ascii')
            img_decode = base64.b64decode(img_decode_)

            result_path = folder_path + "\\" + "result-%05d.jpg"
            with open(result_path, 'wb') as f:
                f.write(img_decode)

    # video file interface
    def process_video_file(self, input_file):

        preprocess.video_resolution_and_bitrate_adjust(input_file, self.b_r_tuple)
        with open(input_file, 'rb') as f:
            img_byte = base64.b64encode(f.read())
            img_str = img_byte.decode('ascii')
        dict = {
            'video_file': img_str
        }
        data = bytes(parse.urlencode(dict), encoding='utf8')
        req = request.Request(url=self.video_file_url, data=data, method='POST')
        # req.add_header("Content-Type", "application/zip")
        response = request.urlopen(req)
        re = response.read().decode('utf-8')

    def initial_network_condition(self):

        cmd = "ping 39.99.145.157 -n 4"
        s = subprocess.getoutput(cmd)
        # print('a')
        last_line = s.split("\n")[-1]
        avg = last_line.split("=")[-1][:-2]
        return avg
        # print(avg)
        # print(s)
        # with open('initial_condition.txt', 'r') as f:
        #     avg_time = f.read()
        # print(avg_time)

        # print('%s' % (t2 - t1))
        # print('#' * 50)


if __name__ == '__main__':

    input_file = "./98368268-1-208.mp4"
    client = Client('video')
    t1 = time.time()
    # client.process_video_file(input_file)
    t2 = time.time()
    # print(t2 - t1)
