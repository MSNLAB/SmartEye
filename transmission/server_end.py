import base64
import os

import cv2
import grpc
import numpy as np
from PIL import Image
from flask import Flask, request, make_response, jsonify

from server.grpc.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import save_file, transfer_file_to_str, transfer_array_and_str
from server import image_classification, object_detection, video_handle_tool

app = Flask(__name__)
# app.DEBUG = True
object_detection_models = [
    'fasterrcnn_mobilenet_v3_large_320_fpn',
    'fasterrcnn_mobilenet_v3_large_fpn',
    'fasterrcnn_resnet50_fpn',
    'maskrcnn_resnet50_fpn',
    'retinanet_resnet50_fpn'
]
image_classification_models = [
    'alexnet', 'densenet', 'densenet121', 'densenet161', 'densenet169',
    'densenet201', 'detection', 'googlenet', 'inception', 'inception_v3',
    'mnasnet', 'mnasnet0_5', 'mnasnet0_75', 'mnasnet1_0', 'mnasnet1_3',
    'mobilenet', 'mobilenet_v2', 'mobilenet_v3_large', 'mobilenet_v3_small',
    'mobilenetv2', 'mobilenetv3', 'quantization', 'resnet', 'resnet101',
    'resnet152', 'resnet18', 'resnet34', 'resnet50', 'resnext101_32x8d',
    'resnext50_32x4d', 'segmentation', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0',
    'shufflenet_v2_x1_5', 'shufflenet_v2_x2_0', 'shufflenetv2', 'squeezenet', 'squeezenet1_0',
    'squeezenet1_1', 'utils', 'vgg', 'vgg11', 'vgg11_bn','vgg13', 'vgg13_bn',
    'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn', 'video', 'wide_resnet101_2', 'wide_resnet50_2'
]
global selected_model


@app.route('/initial', methods=['GET', 'POST'])
def initial():
    """
    do nothing just for testing
    """
    return 'ok'


@app.route('/pictures_handler', methods=['GET', 'POST'])
def pictures_handler():

    info_dict = request.form
    print("mark")
    channel = grpc.insecure_channel('localhost:50051')
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    msg_request = msg_transfer_pb2.MsgRequest(
        model=info_dict["selected_model"], frame=info_dict["frame"], frame_shape=["frame_shape"]
    )
    msg_reply = stub.ImageProcessing(msg_request)
    return
    # selected_model = register_dict['selected_model']
    # frame = register_dict['frame']
    # frame_shape = tuple(int(a) for a in register_dict["frame_shape"][1:-1].split(","))
    # img = transfer_array_and_str(frame, 'down')
    # img = img.reshape(frame_shape)
    # if selected_model in object_detection_models:
    #     frame_handled = object_detection.object_detection_api(img, selected_model, threshold=0.8)
    #     img_str = transfer_array_and_str(frame_handled, 'up')
    #     return jsonify(img_str)
    # else:
    #     result = image_classification.image_classification(img, selected_model)
    #     # print(type(result))
    #     return result


@app.route('/video_file_handler', methods=['GET', 'POST'])
def video_file_handler():

    register_dict = request.form
    selected_model = register_dict['selected_model']
    file__pre_name = register_dict['file_name'].split('.')[0]
    origin_file_path = save_file(**register_dict)
    folder_path = video_handle_tool.extract_frames(origin_file_path)
    picture_list = os.listdir(folder_path)
    if selected_model in object_detection_models:
        for picture in picture_list:
            picture_path = folder_path + "/" + picture
            object_detection.object_detection_api(picture_path, selected_model)
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
    app.run(host='0.0.0.0', port=5000, debug=True)







