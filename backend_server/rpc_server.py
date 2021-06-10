from concurrent import futures
import grpc
import sys

from backend_server.model_controller import load_a_model, get_server_utilization, load_model_files_advance
import globals
sys.path.append("../")
from model_manager import object_detection, image_classification
from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str
from tools.read_config import read_config


object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):
    """gRPC server stub.

    This is a gRPC server stub. Get the request from the gRPC client stub,
    process it and return the result, including image frame, load model request, system info and so on.
    """

    def image_processor(self, request, context):
        """Image process interface.

        Get the image process request from the client, process it and return the result.

        """
        selected_model = request.model
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))
        model = load_a_model(selected_model)
        img = transfer_array_and_str(frame, 'down').reshape(frame_shape)
        msg_reply = image_handler(img, model, selected_model)

        return msg_reply

    def get_server_utilization(self, request, context):
        """Server utilization interface

        Return server utilization to the client.
        """
        server_utilization_reply = get_server_utilization()

        return server_utilization_reply

    def get_loaded_models_name(self, request, context):
        """Loaded model name interface

        Return the loaded model names in the server.
        """
        loaded_model_name_reply = msg_transfer_pb2.Loaded_Model_Name_Reply(
            loaded_model_name=str(globals.loaded_model.keys())
        )
        return loaded_model_name_reply

    def load_specified_model(self, request, context):
        """Load specified model interface.

        Load the specified model as the client request.
        """

        specified_model = request.specified_model
        load_a_model(specified_model)
        load_specified_model_reply = msg_transfer_pb2.load_specified_model_Reply()
        return load_specified_model_reply


def image_handler(img, model, selected_model):
    """Image process function

    :param img: image frame
    :param model: loaded model
    :param selected_model: loaded model name
    :return: processed result
    """

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

    globals.init()
    load_model_files_advance()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
    )
    msg_transfer_pb2_grpc.add_MsgTransferServicer_to_server(
      MsgTransferServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # logging.basicConfig()
    serve()

    # load_model_files_advance().values()
