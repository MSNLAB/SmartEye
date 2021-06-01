import grpc
from server.grpc_config import msg_transfer_pb2_grpc, msg_transfer_pb2


def get_cpu_usage(grpc_server):
    """
    get the cpu usage of grpc server
    :param grpc_server: server's url, including port
    :return: cpu usage
    """
    channel = grpc.insecure_channel(grpc_server)
    stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
    cpu_usage_request = msg_transfer_pb2.Cpu_Usage_Request()
    cpu_usage_reply = stub.Get_Cpu_Usage(cpu_usage_request)
    return cpu_usage_reply.cpu_usage


def get_memory_usage(grpc_server):
    pass


def load_model(grpc_server, model_name):
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
    loaded_model_name_reply = stub.Get_loaded_models_name(loaded_model_name_request)
    loaded_model_name = loaded_model_name_reply.loaded_model_name
    return loaded_model_name
