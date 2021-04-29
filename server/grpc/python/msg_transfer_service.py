import logging
from concurrent import futures

import grpc

from server import object_detection, image_classification
from server.grpc.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str


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


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):

    def ImageProcessing(self, request, context):
        print(1)
        model = request.model
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))

        load_model(model)

        img = transfer_array_and_str(frame, 'down').reshape(frame_shape)
        msg_reply = image_handler(img, model)
        return msg_reply


def load_model(model):
    pass


def image_handler(img, model):

    if model in object_detection_models:
        frame_handled = object_detection.object_detection_api(img, model, threshold=0.8)
        frame_handled_shape = frame_handled.shape
        img_str = transfer_array_and_str(frame_handled, 'up')
        msg_reply = msg_transfer_pb2.MsgReply(
            result=img_str, frame_shape=frame_handled_shape
        )
        return msg_reply
    else:
        result = image_classification.image_classification(img, model)
        msg_reply = msg_transfer_pb2.MsgReply(
            result=result, frame_shape=""
        )
        return msg_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_transfer_pb2_grpc.add_MsgTransferServicer_to_server(
      MsgTransferServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # logging.basicConfig()
    serve()

