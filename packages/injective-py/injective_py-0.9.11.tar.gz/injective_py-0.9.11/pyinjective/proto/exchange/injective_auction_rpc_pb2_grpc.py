# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from exchange import injective_auction_rpc_pb2 as exchange_dot_injective__auction__rpc__pb2


class InjectiveAuctionRPCStub(object):
    """InjectiveAuctionRPC defines gRPC API of the Auction API.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AuctionEndpoint = channel.unary_unary(
                '/injective_auction_rpc.InjectiveAuctionRPC/AuctionEndpoint',
                request_serializer=exchange_dot_injective__auction__rpc__pb2.AuctionEndpointRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__auction__rpc__pb2.AuctionEndpointResponse.FromString,
                )
        self.Auctions = channel.unary_unary(
                '/injective_auction_rpc.InjectiveAuctionRPC/Auctions',
                request_serializer=exchange_dot_injective__auction__rpc__pb2.AuctionsRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__auction__rpc__pb2.AuctionsResponse.FromString,
                )
        self.StreamBids = channel.unary_stream(
                '/injective_auction_rpc.InjectiveAuctionRPC/StreamBids',
                request_serializer=exchange_dot_injective__auction__rpc__pb2.StreamBidsRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__auction__rpc__pb2.StreamBidsResponse.FromString,
                )


class InjectiveAuctionRPCServicer(object):
    """InjectiveAuctionRPC defines gRPC API of the Auction API.
    """

    def AuctionEndpoint(self, request, context):
        """Provide historical auction info for a given auction
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Auctions(self, request, context):
        """Provide the historical auctions info
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamBids(self, request, context):
        """StreamBids streams new bids of an auction.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InjectiveAuctionRPCServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AuctionEndpoint': grpc.unary_unary_rpc_method_handler(
                    servicer.AuctionEndpoint,
                    request_deserializer=exchange_dot_injective__auction__rpc__pb2.AuctionEndpointRequest.FromString,
                    response_serializer=exchange_dot_injective__auction__rpc__pb2.AuctionEndpointResponse.SerializeToString,
            ),
            'Auctions': grpc.unary_unary_rpc_method_handler(
                    servicer.Auctions,
                    request_deserializer=exchange_dot_injective__auction__rpc__pb2.AuctionsRequest.FromString,
                    response_serializer=exchange_dot_injective__auction__rpc__pb2.AuctionsResponse.SerializeToString,
            ),
            'StreamBids': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamBids,
                    request_deserializer=exchange_dot_injective__auction__rpc__pb2.StreamBidsRequest.FromString,
                    response_serializer=exchange_dot_injective__auction__rpc__pb2.StreamBidsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'injective_auction_rpc.InjectiveAuctionRPC', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class InjectiveAuctionRPC(object):
    """InjectiveAuctionRPC defines gRPC API of the Auction API.
    """

    @staticmethod
    def AuctionEndpoint(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_auction_rpc.InjectiveAuctionRPC/AuctionEndpoint',
            exchange_dot_injective__auction__rpc__pb2.AuctionEndpointRequest.SerializeToString,
            exchange_dot_injective__auction__rpc__pb2.AuctionEndpointResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Auctions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_auction_rpc.InjectiveAuctionRPC/Auctions',
            exchange_dot_injective__auction__rpc__pb2.AuctionsRequest.SerializeToString,
            exchange_dot_injective__auction__rpc__pb2.AuctionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamBids(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/injective_auction_rpc.InjectiveAuctionRPC/StreamBids',
            exchange_dot_injective__auction__rpc__pb2.StreamBidsRequest.SerializeToString,
            exchange_dot_injective__auction__rpc__pb2.StreamBidsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
