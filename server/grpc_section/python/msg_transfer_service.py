import os
from concurrent import futures
from torchvision.models import *
from torchvision.models.detection import *
import grpc
import torch
from server import object_detection, image_classification
from server.grpc_section.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str
from tools.read_config import read_config


object_detection_models = [
    'fasterrcnn_mobilenet_v3_large_320_fpn',
    'fasterrcnn_mobilenet_v3_large_fpn',
    'fasterrcnn_resnet50_fpn',
    'maskrcnn_resnet50_fpn',
    'retinanet_resnet50_fpn'
]
image_classification_models = [
    'alexnet', 'densenet121', 'densenet161', 'densenet169',
    'densenet201', 'googlenet', 'inception_v3', 'mnasnet0_5',
    'mnasnet1_0', 'mobilenet_v2', 'mobilenet_v3_large', 'mobilenet_v3_small',
    'resnet101', 'resnet152', 'resnet18', 'resnet34', 'resnet50', 'resnext101_32x8d',
    'resnext50_32x4d', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0', 'squeezenet1_0',
    'squeezenet1_1', 'vgg11', 'vgg11_bn','vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn',
    'vgg19', 'vgg19_bn', 'wide_resnet101_2', 'wide_resnet50_2'
]


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):

    def ImageProcessing(self, request, context):
        selected_model = request.model
        # print(selected_model)
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))
        # print(len(frame))
        model = load_model(selected_model)
        img = transfer_array_and_str(frame, 'down').reshape(frame_shape)
        msg_reply = image_handler(img, model, selected_model)

        return msg_reply


def load_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """

    preload_models = read_config("preload-models")
    if selected_model in preload_models:
        model = eval(selected_model)()
        model.load_state_dict(result_dict[selected_model], False)
    # print(model)
    else:
        weight_folder = read_config("models-path", "path")
        try:
            for file in os.listdir(weight_folder):
                if selected_model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            print("there is no matched file!")
        # print(selected_model)
        weight_files_path = os.path.join(weight_folder, file_name)
        model = eval(selected_model)()
        model.load_state_dict(torch.load(weight_files_path), False)
    model.eval()
    return model


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
        result = image_classification.image_classification(img, model)
        msg_reply = msg_transfer_pb2.MsgReply(
            result=result, frame_shape=""
        )
        return msg_reply


def serve():

    global result_dict
    result_dict = load_model_files_advance()
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
    weight_folder = read_config("models-path", "path")
    preload_models = read_config("preload-models")
    load_file_result_dict = {}

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
        load_file_result_dict[model] = file_load
    return load_file_result_dict



if __name__ == '__main__':
    # logging.basicConfig()
    # serve()
    load_model_files_advance().values()
