import grpc
from flask import Flask, request, make_response, jsonify

from server.grpc.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2

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
    channel = grpc.insecure_channel('localhost:50051')
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    msg_request = msg_transfer_pb2.MsgRequest(
        model=info_dict["selected_model"], frame=info_dict["frame"], frame_shape=info_dict["frame_shape"]
    )
    msg_reply = stub.ImageProcessing(msg_request)
    print(1)
    if msg_reply.frame_shape == "":
        return msg_reply.result
    else:
        return msg_reply.result

