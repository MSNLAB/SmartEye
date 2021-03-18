from urllib import request, parse
import base64
import time
import extractframes
import os
import preproccess
import mmap


#url = 'http://39.99.145.157:5000/hello'
class client:
    """
    Serve as the AR client
    """


    def __init__(self):

        # self.input_file = input_file
        print("mark")
        self.initial_url = "http://39.99.145.157:5000/initial"
        self.picture_url = "http://39.99.145.157:5000/pictures_handler"
        self.video_file_url = "http://39.99.145.157:5000/video_file_handler"
        self.service_delay = 0
        self.requirements = 0
        self.netcondition = 0

        # send initial condition to the server
        dict = {
            'service_delay': self.service_delay,
            'requirements': self.requirements,
            'netcondition': self.netcondition
        }
        headers = {
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }
        data = bytes(parse.urlencode(dict), encoding='utf8')
        req = request.Request(url=self.initial_url, data=data, headers=headers, method='POST')

        response = request.urlopen(req)
        self.image_size = response.read().decode('utf-8')
        # print('mark2')
        print(self.image_size)

    # picture interface
    def proccess_picture(self, input_file):

        headers = {
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }
        # t1 = time.time()
        # read pictures one by one from the picture folder
        folder_path = extractframes.extract_frames(input_file)
        # t2 = time.time()
        picture_list = os.listdir(folder_path)
        # print(picture_list)
        for picture in picture_list:
            picture_path = folder_path + "\\" + picture
            preproccess.image_size_adjust(image_size=self.image_size, input_file=picture_path)
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
    def proccess_video_file(self, input_file):

        f = open(input_file, 'rb')
        mmapped_file_as_string = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        dict = {
            'video_file': mmapped_file_as_string
        }
        data = bytes(parse.urlencode(dict), encoding='utf8')
        req = request.Request(url=self.video_file_url, data=data)
        req.add_header("Content-Type", "application/zip")
        response = request.urlopen(req)
        print(response.read().decode('utf-8'))
        # close everything
        mmapped_file_as_string.close()
        f.close()





        # print('%s' % (t2 - t1))
        # print('#' * 50)

if __name__ == '__main__':


    input_file = "D:\\Ubuntu_1804.2019.522.0_x64\\rootfs\home\wxz\Documents\\video2edge\85652500-1-192.mp4"
    client = client()
    client.proccess_video_file(input_file)