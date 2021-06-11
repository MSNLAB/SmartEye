import sys
from dispatch_policy import random_policy, shortest_queue, lowest_cpu_utilization
from frontend_server.grpc_interface import get_grpc_reply
import globals
from frontend_server.monitor import server_monitor
from tools.read_config import read_config
from loguru import logger
sys.path.append("../")
from flask import Flask, request, jsonify
import time
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
sched.add_job(server_monitor, 'interval', seconds=int(read_config("monitor", "monitor_interval")))
sched.start()

logger.add("transfer-server_{time}.log")


@app.route('/image_handler', methods=['GET', 'POST'])
def image_handler():
    """Images transfer interface.


    Get info sent from local and transfer it to processing servers,
    then collect the processing result returned from grpc server
    and return the result to the client.

    :return: return_dict
    """
    info_dict = request.form
    server_url = rpc_server_selection("random")
    globals.tasks_number[server_url] += 1
    t1 = time.time()
    try:
        msg_reply = get_grpc_reply(server_url, **info_dict)
    except Exception as err:
        logger.exception("Get result error:", err)
    globals.tasks_number[server_url] -= 1
    t2 = time.time()
    if msg_reply is None:
        return None
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
    """Select a grpc server to which info will send.

    :param policy decide the policy of selecting a grpc server
    :return: server url
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
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
