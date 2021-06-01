import os
from concurrent import futures
import grpc
import torch
import sys

from flask import jsonify

from server.model_operation import load_model, get_server_cpu_usage, uninstall_model
import global_variable
sys.path.append("../")
from model_manager import object_detection, image_classification
from server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str
from tools.read_config import read_config
import psutil

object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):

    def ImageProcessing(self, request, context):

        selected_model = request.model
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))
        model = load_model(selected_model)
        img = transfer_array_and_str(frame, 'down').reshape(frame_shape)
        msg_reply = image_handler(img, model, selected_model)

        return msg_reply

    def Get_Cpu_Usage(self, request, context):

        cpu_usage_reply = get_server_cpu_usage()

        return cpu_usage_reply

    def Get_loaded_models_name(self, request, context):

        loaded_model_name_reply = msg_transfer_pb2.Loaded_Model_Name_Reply(
            loaded_model_name=str(global_variable.loaded_model_dict.keys())
        )
        return loaded_model_name_reply

    def load_specified_model(self, request, context):

        specified_model = request.specified_model
        load_model(specified_model)
        load_specified_model_reply = msg_transfer_pb2.load_specified_model_Reply()
        return load_specified_model_reply


def image_handler(img, model, selected_model):

    if selected_model in object_detection_models:
        frame_handled = object_detection.object_detection_api(img, model, threshold=0.8)
        frame_handled_shape = str(frame_handled.shape)
        img_str = transfer_array_and_str(frame_handled, 'up')
        msg_reply = msg_transfer_pb2.MsgReply(
            result=img_str, frame_shape=frame_handled_shape
        )
        # print(len(img_str))
        return msg_reply
    else:
        result = image_classification.image_classification(img, selected_model)
        msg_reply = msg_transfer_pb2.MsgReply(
            result=result, frame_shape=""
        )
        return msg_reply


def serve():

    global_variable.init()
    load_model_files_advance()
    # MAX_MESSAGE_LENGTH =
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        # options=[
        #     ('grpc.max_send_message_length', 256 * 1024 * 1024),
        #     ('grpc.max_receive_message_length', 256 * 1024 * 1024),
        # ]
    )
    msg_transfer_pb2_grpc.add_MsgTransferServicer_to_server(
      MsgTransferServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def load_model_files_advance():
    """
    load model files in advance into memory
    :return:
    """
    # weight_folder = read_config("models-path", "path")
    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    preload_models = read_config("preload-models")
    global loaded_model_dict
    loaded_model_dict = {}

    for model in preload_models:
        try:
            for file in os.listdir(weight_folder):
                if model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            print("there is no matched file!")
        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        global_variable.loaded_model_dict[model] = file_load


if __name__ == '__main__':
    # logging.basicConfig()
    serve()

    # load_model_files_advance().values()
