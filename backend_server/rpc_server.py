from concurrent import futures
import grpc
import sys

from backend_server.model_controller import load_a_model, get_server_cpu_usage, load_model_files_advance
import global_variable
sys.path.append("../")
from model_manager import object_detection, image_classification
from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.transfer_files_tool import transfer_array_and_str
from tools.read_config import read_config

object_detection_models = read_config("object-detection")
image_classification_models = read_config("image-classification")


class MsgTransferServer(msg_transfer_pb2_grpc.MsgTransferServicer):

    def image_processor(self, request, context):

        selected_model = request.model
        frame = request.frame
        frame_shape = tuple(int(s) for s in request.frame_shape[1:-1].split(","))
        model = load_a_model(selected_model)
        img = transfer_array_and_str(frame, 'down').reshape(frame_shape)
        msg_reply = image_handler(img, model, selected_model)

        return msg_reply

    def get_server_utilization(self, request, context):

        cpu_usage_reply = get_server_cpu_usage()

        return cpu_usage_reply

    def get_loaded_models_name(self, request, context):

        loaded_model_name_reply = msg_transfer_pb2.Loaded_Model_Name_Reply(
            loaded_model_name=str(global_variable.loaded_model_dict.keys())
        )
        return loaded_model_name_reply

    def load_specified_model(self, request, context):

        specified_model = request.specified_model
        load_a_model(specified_model)
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


if __name__ == '__main__':
    # logging.basicConfig()
    serve()

    # load_model_files_advance().values()
