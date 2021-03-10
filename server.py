import json
import cv2
from flask import Flask, request, make_response, Response, render_template, jsonify
import objectdetection
# base64编解码
import base64
import numpy as np
import matplotlib.pyplot as plt


# print(__name__)
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello_world():

    # 传输算法名称
    register_dict = request.form

    name = register_dict['name']
    image_str = register_dict['image']

    img_decode_ = image_str.encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    with open('girl.jpg', 'wb') as f:
        f.write(img_decode)

    objectdetection.object_detection_api('./girl.jpg', threshold=0.8)
    with open('meelo.jpg', 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
        img_str = img_byte.decode('ascii')
    response = make_response(img_str)
    return response

    # img_ = open("meelo.jpg", encoding='utf-8', errors='ignore').read()
    # print(type(img_))
    # response = Response(img_, mimetype="image/jpeg")

    # with open("meelo.jpg", "rb") as f:
    #     b64image = base64.b64encode(f.read())
    # img_data = base64.b64decode(b64image)

    # response.headers.set('Content-Type', "image/jpeg")  # 设置content-type
    # response.headers.set(
    #     'Content-Disposition', 'attachment')  # 告诉浏览器进行下载
    # response.headers.set('Cache-Control', 'max-age=86400')  # 缓存超时时间




if __name__ == '__main__':
    app.run()

# 备选1
# img = cv2.imdecode(img_np_, cv2.COLOR_RGB2BGR)  # 转为opencv格式
# cv2.imshow('frame', img)
# cv2.waitKey()
# upload_file = request.get_data()
#     req = json.loads(upload_file)
#     if upload_file:
#         name = req['name']
#         print(name)
#         img_str = req['image']  # 得到unicode的字符串
#         img_decode_ = img_str.encode('ascii')  # 从unicode变成ascii编码
#         img_decode = base64.b64decode(img_decode_)  # 解base64编码，得图片的二进制
#         img_np_ = np.frombuffer(img_decode, np.uint8)
#         print(img_np_.shape)