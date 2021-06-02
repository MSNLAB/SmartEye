import grpc
import sys
from dispatch_policy import random_policy

from transmission.get_grpc_info import get_server_utilization, load_specified_model, get_loaded_models

sys.path.append("../")
from flask import Flask, request, jsonify
import time
from server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from tools.read_config import read_config
import random

app = Flask(__name__)


@app.route('/image_handler', methods=['GET', 'POST'])
def image_handler():
    """
    get info from local and then transfer to processing servers
    :return:
    """

    info_dict = request.form
    server_url = rpc_server_selection()
    t1 = time.time()
    msg_reply = get_result(server_url, **info_dict)
    t2 = time.time()
    if msg_reply.frame_shape == "":
        return_dict = {
            "prediction": msg_reply.result,
            "process_time": t2 - t1
        }

        return jsonify(return_dict)

    else:
        return_dict = {
            "frame_shape": msg_reply.frame_shape,
            "result": msg_reply.result,
            "process_time": t2 - t1
        }

        return jsonify(return_dict)


def rpc_server_selection():
    """
    decide which server to send frame to
    :return: server number
    """
    grpc_server = random_policy()
    return grpc_server


def get_result(server_url, **info_dict):
    """
    send frame to handled server whose server number equals to server_number, get return the result struct
    :param server_url: handled servers' url
    :return: msg_reply
    """

    options = [('grpc.max_receive_message_length', 256 * 1024 * 1024)]
    channel = grpc.insecure_channel(server_url, options=options)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    msg_request = msg_transfer_pb2.MsgRequest(
        model=info_dict["selected_model"], frame=info_dict["frame"], frame_shape=info_dict["frame_shape"]
    )
    msg_reply = stub.image_processor(msg_request)
    return msg_reply


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
