# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from exchange import injective_accounts_rpc_pb2 as exchange_dot_injective__accounts__rpc__pb2


class InjectiveAccountsRPCStub(object):
    """InjectiveAccountsRPC defines API of Exchange Accounts provider.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Portfolio = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/Portfolio',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.PortfolioRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.PortfolioResponse.FromString,
                )
        self.OrderStates = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/OrderStates',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.OrderStatesRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.OrderStatesResponse.FromString,
                )
        self.SubaccountsList = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountsList',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountsListRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountsListResponse.FromString,
                )
        self.SubaccountBalancesList = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountBalancesList',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListResponse.FromString,
                )
        self.SubaccountBalanceEndpoint = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountBalanceEndpoint',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointResponse.FromString,
                )
        self.StreamSubaccountBalance = channel.unary_stream(
                '/injective_accounts_rpc.InjectiveAccountsRPC/StreamSubaccountBalance',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceResponse.FromString,
                )
        self.SubaccountHistory = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountHistory',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryResponse.FromString,
                )
        self.SubaccountOrderSummary = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountOrderSummary',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryResponse.FromString,
                )
        self.Rewards = channel.unary_unary(
                '/injective_accounts_rpc.InjectiveAccountsRPC/Rewards',
                request_serializer=exchange_dot_injective__accounts__rpc__pb2.RewardsRequest.SerializeToString,
                response_deserializer=exchange_dot_injective__accounts__rpc__pb2.RewardsResponse.FromString,
                )


class InjectiveAccountsRPCServicer(object):
    """InjectiveAccountsRPC defines API of Exchange Accounts provider.
    """

    def Portfolio(self, request, context):
        """Provide the account's portfolio value in USD.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderStates(self, request, context):
        """List order states by order hashes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountsList(self, request, context):
        """List all subaccounts IDs of an account address
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountBalancesList(self, request, context):
        """List subaccount balances for the provided denoms.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountBalanceEndpoint(self, request, context):
        """Gets a balance for specific coin denom
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamSubaccountBalance(self, request, context):
        """StreamSubaccountBalance streams new balance changes for a specified
        subaccount and denoms. If no denoms are provided, all denom changes are
        streamed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountHistory(self, request, context):
        """Get subaccount's deposits and withdrawals history
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountOrderSummary(self, request, context):
        """Get subaccount's orders summary
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Rewards(self, request, context):
        """Provide historical trading rewards
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InjectiveAccountsRPCServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Portfolio': grpc.unary_unary_rpc_method_handler(
                    servicer.Portfolio,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.PortfolioRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.PortfolioResponse.SerializeToString,
            ),
            'OrderStates': grpc.unary_unary_rpc_method_handler(
                    servicer.OrderStates,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.OrderStatesRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.OrderStatesResponse.SerializeToString,
            ),
            'SubaccountsList': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountsList,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountsListRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountsListResponse.SerializeToString,
            ),
            'SubaccountBalancesList': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountBalancesList,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListResponse.SerializeToString,
            ),
            'SubaccountBalanceEndpoint': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountBalanceEndpoint,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointResponse.SerializeToString,
            ),
            'StreamSubaccountBalance': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamSubaccountBalance,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceResponse.SerializeToString,
            ),
            'SubaccountHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountHistory,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryResponse.SerializeToString,
            ),
            'SubaccountOrderSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountOrderSummary,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryResponse.SerializeToString,
            ),
            'Rewards': grpc.unary_unary_rpc_method_handler(
                    servicer.Rewards,
                    request_deserializer=exchange_dot_injective__accounts__rpc__pb2.RewardsRequest.FromString,
                    response_serializer=exchange_dot_injective__accounts__rpc__pb2.RewardsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'injective_accounts_rpc.InjectiveAccountsRPC', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class InjectiveAccountsRPC(object):
    """InjectiveAccountsRPC defines API of Exchange Accounts provider.
    """

    @staticmethod
    def Portfolio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/Portfolio',
            exchange_dot_injective__accounts__rpc__pb2.PortfolioRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.PortfolioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OrderStates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/OrderStates',
            exchange_dot_injective__accounts__rpc__pb2.OrderStatesRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.OrderStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubaccountsList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountsList',
            exchange_dot_injective__accounts__rpc__pb2.SubaccountsListRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.SubaccountsListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubaccountBalancesList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountBalancesList',
            exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.SubaccountBalancesListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubaccountBalanceEndpoint(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountBalanceEndpoint',
            exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.SubaccountBalanceEndpointResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamSubaccountBalance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/StreamSubaccountBalance',
            exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.StreamSubaccountBalanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubaccountHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountHistory',
            exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.SubaccountHistoryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubaccountOrderSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/SubaccountOrderSummary',
            exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.SubaccountOrderSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Rewards(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/injective_accounts_rpc.InjectiveAccountsRPC/Rewards',
            exchange_dot_injective__accounts__rpc__pb2.RewardsRequest.SerializeToString,
            exchange_dot_injective__accounts__rpc__pb2.RewardsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
