import sys
from dispatch_policy import random_policy, shortest_queue, lowest_cpu_utilization
from frontend_server.grpc_interface import get_grpc_reply   #get_server_utilization, load_specified_model, get_loaded_models,
import globals
sys.path.append("../")
from flask import Flask, request, jsonify
import time
# from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
# from tools.read_config import read_config
# import random


app = Flask(__name__)


@app.route('/image_handler', methods=['GET', 'POST'])
def image_handler():
    """
    get info from local and then transfer to processing servers
    :return:
    """
    info_dict = request.form
    server_url = rpc_server_selection("random")
    globals.tasks_number[server_url] += 1
    t1 = time.time()
    msg_reply = get_grpc_reply(server_url, **info_dict)
    globals.tasks_number[server_url] -= 1
    t2 = time.time()
    if msg_reply.frame_shape == "":
        return_dict = {
            "prediction": msg_reply.result,
            "process_time": t2 - t1}
        return jsonify(return_dict)
    else:
        return_dict = {
            "frame_shape": msg_reply.frame_shape,
            "result": msg_reply.result,
            "process_time": t2 - t1}
        return jsonify(return_dict)


def rpc_server_selection(policy):
    """
    decide which server to send frame to
    :return: server number
    """
    if policy == 'random':
        grpc_server = random_policy()
    elif policy == 'tasks_queue':
        grpc_server = shortest_queue()
    else:
        grpc_server = lowest_cpu_utilization()
    return grpc_server


if __name__ == '__main__':

    globals.init()
    # print(globals.tasks_number_dict)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
