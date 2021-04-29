import logging

import grpc
from server.grpc.pbfile import msg_transfer_pb2_grpc, msg_transfer_pb2


def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = msg_transfer_pb2_grpc.MsgTransferStub(channel)
        stub.ImageProcessing(msg_transfer_pb2.MsgRequest(model='a', image='s'))
        print("client")


if __name__ == '__main__':
    # logging.basicConfig()

    run()
