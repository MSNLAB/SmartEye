import os

import cv2
from flask import Flask, request, make_response, Response, render_template
import objectdetection
import base64
import numpy as np
import matplotlib.pyplot as plt
import time
from decision_engine import DecisionEngine
import extractframes
from transfer_files_tool import save_file, transfer_file_to_str

app = Flask(__name__)
global selected_model


class Server:

    @app.route('/initial', methods=['GET', 'POST'])
    def initial(self):
        initial_dict = request.form
        selected_model = initial_dict['selected_model']
        # response = make_response(str(send_back_msg))
        # return response

    @app.route('/pictures_handler', methods=['GET', 'POST'])
    def pictures_handler(self):

        register_dict = request.form
        origin_file_path = save_file(register_dict['image'])
        # t1 = time.time()
        handled_file_path = objectdetection.object_detection_api(origin_file_path, threshold=0.8)
        # t2 = time.time()
        # print('%s' % (t2 - t1))
        # print('#' * 50)
        img_str = transfer_file_to_str(handled_file_path)
        response = make_response(img_str)
        return response

    @app.route('/video_file_handler', methods=['GET', 'POST'])
    def video_file_handler(self):

        register_dict = request.form
        origin_file_path = save_file(register_dict['video'])
        folder_path = extractframes.extract_frames(origin_file_path)
        picture_list = os.listdir(folder_path)
        for picture in picture_list:
            picture_path = folder_path + "\\" + picture
        response = make_response('ok')
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)







