import cv2
from flask import Flask, request, make_response, Response, render_template
import objectdetection
import base64
import numpy as np
import matplotlib.pyplot as plt
import time
from decision_engine import DecisionEngine

app = Flask(__name__)


@app.route('/initial', methods=['GET', 'POST'])
def initial():

    initial_dict = request.form
    # service_delay = initial_dict['service_delay']
    # requirements = initial_dict['requirements']
    # net_condition =initial_dict['net_condition']

    send_back_msg, selected_model = DecisionEngine(**initial_dict)

    response = make_response(str(send_back_msg))
    return response


@app.route('/pictures_handler', methods=['GET', 'POST'])
def pictures_handler():

    # get selected algorithm name
    register_dict = request.form
    name = register_dict['name']

    # get image information and decode
    image_str = register_dict['image']
    img_decode_ = image_str.encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    # save the information as .jpg file
    with open('girl.jpg', 'wb') as f:
        f.write(img_decode)
    # object detection
    t1 = time.time()
    # of course, there are some preproccess action should be done
    objectdetection.object_detection_api('./girl.jpg', threshold=0.8)
    t2 = time.time()
    print('%s' % (t2 - t1))
    print('#' * 50)
    with open('meelo.jpg', 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
        img_str = img_byte.decode('ascii')
    response = make_response(img_str)
    return response


@app.route('/video_file_handler', methods=['GET', 'POST'])
def video_file_handler():

    register_dict = request.form
    video_file = register_dict['video_file']
    img_decode_ = video_file.encode('ascii')
    img_decode = base64.b64decode(img_decode_)
    # print(video_file)
    with open('girl.mp4', 'wb') as f:
        f.write(img_decode)
    # message = register_dict.values()
    response = make_response('ok')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)







