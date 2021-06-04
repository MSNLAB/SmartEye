import grpc
from backend_server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2


def get_grpc_reply(server_url, **info_dict):
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


def get_server_utilization(grpc_server):
    """
    get the cpu usage of grpc server
    :param grpc_server: server's url, including port
    :return: cpu usage
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    server_utilization_request = msg_transfer_pb2.Server_Utilization_Request()
    server_utilization_reply = stub.get_server_utilization(server_utilization_request)
    return server_utilization_reply.cpu_usage, server_utilization_reply.memory_usage


def load_specified_model(grpc_server, model_name):
    """
    request grpc server to load the specified model
    :param grpc_server: server url
    :param model_name: model name
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    load_specified_model_request = msg_transfer_pb2.load_specified_model_Request(
        specified_model=model_name)
    stub.load_specified_model(load_specified_model_request)


def get_loaded_models(grpc_server):
    """
    get the loaded models' name from the server
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    loaded_model_name_request = msg_transfer_pb2.Loaded_Model_Name_Request()
    loaded_model_name_reply = stub.get_loaded_models_name(loaded_model_name_request)
    loaded_model_name = loaded_model_name_reply.loaded_model_name
    return loaded_model_name
