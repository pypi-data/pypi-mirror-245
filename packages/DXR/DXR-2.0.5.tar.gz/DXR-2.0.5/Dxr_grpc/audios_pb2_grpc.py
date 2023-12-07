# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import audios_pb2 as audios__pb2


class MainServerStub(object):
    """responce server
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getStream = channel.stream_stream(
                '/MainServer/getStream',
                request_serializer=audios__pb2.Request.SerializeToString,
                response_deserializer=audios__pb2.Reply.FromString,
                )


class MainServerServicer(object):
    """responce server
    """

    def getStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MainServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getStream': grpc.stream_stream_rpc_method_handler(
                    servicer.getStream,
                    request_deserializer=audios__pb2.Request.FromString,
                    response_serializer=audios__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MainServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MainServer(object):
    """responce server
    """

    @staticmethod
    def getStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/MainServer/getStream',
            audios__pb2.Request.SerializeToString,
            audios__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
