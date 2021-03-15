from urllib import request, parse
import base64
import time
import extractframes
import os


#url = 'http://39.99.145.157:5000/hello'
class client:
    """
    Serve as the AR client
    """


    def __init__(self,input_file, url):

        self.input_file = input_file
        self.url = url

    def proccess(self):


        headers = {
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 'Host': 'httpbin.org'
        }
        # t1 = time.time()
        # read pictures one by one from the picture folder
        folder_path = extractframes.extract_frames(self.input_file)
        # t2 = time.time()
        picture_list = os.listdir(folder_path)
        # print(picture_list)
        for picture in picture_list:
            picture_path = folder_path + "\\" + picture
            with open(picture_path, 'rb') as f:
                img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
                img_str = img_byte.decode('ascii')
            dict = {
                'name': 'Germey',
                'image': img_str
            }
            data = bytes(parse.urlencode(dict), encoding='utf8')
            req = request.Request(url=self.url, data=data, headers=headers, method='POST')

            response = request.urlopen(req)
            img = response.read().decode('utf-8')
            img_decode_ = img.encode('ascii')
            img_decode = base64.b64decode(img_decode_)

            result_path = folder_path + "\\" + "result-%05d.jpg"
            with open(result_path, 'wb') as f:
                f.write(img_decode)




        # print('%s' % (t2 - t1))
        # print('#' * 50)

if __name__ == '__main__':

    url = 'http://39.99.145.157:5000/hello'
    input_file = "D:\\Ubuntu_1804.2019.522.0_x64\\rootfs\home\wxz\Documents\\video2edge\85652500-1-192.mp4"
    client = client(input_file, url)
    client.proccess()