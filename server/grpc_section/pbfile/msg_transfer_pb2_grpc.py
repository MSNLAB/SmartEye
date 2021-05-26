# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from server.grpc_section.protos import msg_transfer_pb2 as server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2


class MsgTransferStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ImageProcessing = channel.unary_unary(
                '/MsgTransfer/ImageProcessing',
                request_serializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgRequest.SerializeToString,
                response_deserializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgReply.FromString,
                )
        self.Get_Cpu_Usage = channel.unary_unary(
                '/MsgTransfer/Get_Cpu_Usage',
                request_serializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Request.SerializeToString,
                response_deserializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Reply.FromString,
                )


class MsgTransferServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ImageProcessing(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_Cpu_Usage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgTransferServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ImageProcessing': grpc.unary_unary_rpc_method_handler(
                    servicer.ImageProcessing,
                    request_deserializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgRequest.FromString,
                    response_serializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgReply.SerializeToString,
            ),
            'Get_Cpu_Usage': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_Cpu_Usage,
                    request_deserializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Request.FromString,
                    response_serializer=server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MsgTransfer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MsgTransfer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ImageProcessing(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MsgTransfer/ImageProcessing',
            server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgRequest.SerializeToString,
            server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.MsgReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_Cpu_Usage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MsgTransfer/Get_Cpu_Usage',
            server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Request.SerializeToString,
            server_dot_grpc__section_dot_protos_dot_msg__transfer__pb2.Cpu_Usage_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
