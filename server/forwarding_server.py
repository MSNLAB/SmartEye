import grpc
from torchvision.models import *
from torchvision.models.detection import *
from tools.read_config import read_config
from flask import Flask, request, jsonify

from server.grpc_section.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2

app = Flask(__name__)


@app.route('/initial', methods=['GET', 'POST'])
def initial():
    """
    do nothing just for testing
    """
    return 'ok'


@app.route('/pictures_handler', methods=['GET', 'POST'])
def pictures_handler():
    """
    get info from client and then transfer to processing servers
    :return:
    """
    info_dict = request.form
    # options = [('grpc.max_message_length', 256 * 1024 * 1024)]

    options = [('grpc.max_receive_message_length', 256 * 1024 * 1024)]
    grpc_url = read_config("grpc-url", "url1")
    channel = grpc.insecure_channel(grpc_url, options=options)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    msg_request = msg_transfer_pb2.MsgRequest(
        model=info_dict["selected_model"], frame=info_dict["frame"], frame_shape=info_dict["frame_shape"]
    )
    msg_reply = stub.ImageProcessing(msg_request)
    if msg_reply.frame_shape == "":
        return msg_reply.result
    else:
        return_dict = {
            "frame_shape": msg_reply.frame_shape,
            "result": msg_reply.result
        }

        return jsonify(return_dict)

