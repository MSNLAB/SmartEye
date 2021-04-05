import os
import cv2
from flask import Flask, request, make_response, Response, render_template, jsonify
import objectdetection
import base64
import numpy as np
import matplotlib.pyplot as plt
import time
import video_handle_tool
from transfer_files_tool import save_file, transfer_file_to_str
import image_classification

app = Flask(__name__)
object_detection_models = ['fasterrcnn_mobilenet_v3_large_320_fpn', 'fasterrcnn_mobilenet_v3_large_fpn',
                                        'fasterrcnn_resnet50_fpn', 'maskrcnn_resnet50_fpn', 'retinanet_resnet50_fpn']
image_classification_models = []
global selected_model


@app.route('/initial', methods=['GET', 'POST'])
def initial(self):
    """
    do nothing just for testing
    """
    return 'ok'


@app.route('/pictures_handler', methods=['GET', 'POST'])
def pictures_handler(self):

    register_dict = request.form
    selected_model = register_dict['selected_model']
    origin_file_path = save_file(**register_dict)
    # t1 = time.time()
    if selected_model in object_detection_models:
        handled_file_path = objectdetection.object_detection_api(origin_file_path, selected_model, threshold=0.8)
        msg_dict = transfer_file_to_str(handled_file_path)
        return jsonify(msg_dict)
    else:
        result = image_classification.image_classification(origin_file_path, selected_model)
        return result


@app.route('/video_file_handler', methods=['GET', 'POST'])
def video_file_handler(self):

    register_dict = request.form
    selected_model = register_dict['selected_model']
    file__pre_name = register_dict['file_name'].split('.')[0]
    origin_file_path = save_file(**register_dict)
    folder_path = video_handle_tool.extract_frames(origin_file_path)
    picture_list = os.listdir(folder_path)
    if selected_model in object_detection_models:
        for picture in picture_list:
            picture_path = folder_path + "/" + picture
            objectdetection.object_detection_api(picture_path, selected_model)
        processed_files_folder = folder_path + '/' + file__pre_name + '_processed/' + file__pre_name + "-%05d.jpg"
        video_path = video_handle_tool.compose_video(processed_files_folder, origin_file_path)
        img_str = transfer_file_to_str(video_path)
        response = make_response(img_str)
        return response
    else:
        result_list = []
        for picture in picture_list:
            picture_path = folder_path + "/" + picture
            result = image_classification.image_classification(picture_path, selected_model)
            result_list.append(result)
        response = make_response(str(result_list))
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)







