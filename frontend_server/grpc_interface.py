import grpc
from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2
from loguru import logger


def get_grpc_reply(server_url, **info_dict):
    """Send frame to server and get result.

    Send frame to processing server whose server number equals to server_number,
    and get the result.

    :param server_url: processing servers' url
    :param info_dict: info sent from client, including selected_model, frame_shape and frame
    :return: msg_reply: a data structure of grpc
    """

    options = [('grpc.max_receive_message_length', 256 * 1024 * 1024)]
    channel = grpc.insecure_channel(server_url, options=options)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    msg_request = msg_transfer_pb2.MsgRequest(
        model=info_dict["selected_model"], frame=info_dict["frame"], frame_shape=info_dict["frame_shape"]
    )
    try:
        msg_reply = stub.image_processor(msg_request, timeout=1)
    except:
        logger.exception("Error: GRPC reply error!")
        pass
    else:
        return msg_reply


def get_server_utilization(grpc_server):
    """Get the cpu usage of grpc server

    :param grpc_server: server's url, including port
    :return: the server's cpu usage
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    server_utilization_request = msg_transfer_pb2.Server_Utilization_Request()
    try:
        server_utilization_reply = stub.get_server_utilization(server_utilization_request)
    except TimeoutError as err:
        logger.exception("Get server utilization error:", err)
    return server_utilization_reply.cpu_usage, server_utilization_reply.memory_usage


def load_specified_model(grpc_server, model_name):
    """Request a specified grpc server to load a specified model

    :param grpc_server: server url
    :param model_name: model name
    :return: None
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    load_specified_model_request = msg_transfer_pb2.load_specified_model_Request(
        specified_model=model_name)
    try:
        stub.load_specified_model(load_specified_model_request, timeout=10)
    except Exception as err:
        logger.exception("Load specified model error:", err)


def get_loaded_models(grpc_server):
    """Get the loaded models' name from the server

    :param grpc_server: server url
    :return: loaded model list
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    loaded_model_name_request = msg_transfer_pb2.Loaded_Model_Name_Request()
    try:
        loaded_model_name_reply = stub.get_loaded_models_name(loaded_model_name_request, timeout=10)
    except Exception as err:
        logger.exception("Get loaded model error:", err)
    loaded_model_name = loaded_model_name_reply.loaded_model_name
    return loaded_model_name
